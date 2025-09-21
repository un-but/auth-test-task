"""Файл конфигурации всех частей приложения.

В модуле определена строгая иерархия, которой следует придерживаться.

Основный классом настроек является Config, для которого создается единственный экземпляр config,
который следует импортировать для доступа к конфигурации.

В классе Config все поля - классы pydantic, при инициализации в него нельзя передавать значения.

В Config все поля являются значениями в которых у всех полей должны быть значения
from_source(Source.{ИСТОЧНИК_ПОЛЯ})
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, SecretStr
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


# Функция для создания поля с указанием источника
def from_source(source: Literal["env", "toml"], default: Any = ..., **kwargs: Any) -> Any:
    """Создает поле с учетом источника данных.

    Args:
        source (Source): источник данных.
        default (Source, optional): значение поля по умолчанию. Если не указано то ...
        kwargs (Any): аргументы передаваемые в Field из Pydantic

    Returns:
        Any: значение поля

    """
    return Field(default, json_schema_extra={"source": source}, **kwargs)


########## Модели данных ##########


class APIConfig(BaseModel):
    """Настройки FastAPI приложения."""

    name: str = from_source("toml")

    jwt_secret: SecretStr = from_source("env")
    jwt_access_expire_seconds: int = from_source("toml")
    jwt_refresh_expire_days: int = from_source("toml")


class DatabaseConfig(BaseModel):
    """Настройки работы с базой данных через SQLAlchemy."""

    ps_url: SecretStr = from_source("env")
    rd_url: SecretStr = from_source("env")
    echo: bool = from_source("toml")


########## Класс настроек ##########


class Config(BaseSettings):
    """Создает объект с настройками приложения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api: APIConfig
    database: DatabaseConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        class TomlSource(PydanticBaseSettingsSource):
            def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
                return super().get_field_value(field, field_name)

            def __call__(self) -> dict[str, Any]:
                with Path("config.toml").open("rb") as f:
                    return tomllib.load(f)

        class EnvSource(PydanticBaseSettingsSource):
            def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
                return super().get_field_value(field, field_name)

            def __call__(self) -> dict[str, Any]:
                return {
                    field_name: self._parse_sub_fields(field, field_name)
                    for field_name, field in settings_cls.model_fields.items()
                }

            def _parse_sub_fields(self, field: FieldInfo, field_name: str) -> dict[str, Any]:
                try:
                    return {
                        sub_field_name: os.environ[f"{field_name}_{sub_field_name}".upper()]
                        for sub_field_name, sub_field in field.annotation.model_fields.items()
                        if sub_field.json_schema_extra.get("source") == "env"
                        and f"{field_name}_{sub_field_name}".upper() in os.environ
                    }
                except AttributeError:  # Если у полей не указан источник
                    error_msg = "Нарушены правила работы с конфигом, описанные в начале модуля"
                    raise AttributeError(error_msg)

        return (EnvSource(settings_cls), TomlSource(settings_cls))


config = Config()

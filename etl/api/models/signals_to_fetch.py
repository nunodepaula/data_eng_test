"""Entidade de lista de sinais usada na rota de obtenção de dados.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from pydantic import BaseModel, ValidationError, field_validator


class Signals2Fetch(BaseModel):
    """Modelo de validação da lista de sinais usadas na rota de obtenção de dados.

    Raises:
        ValidationError: Caso a lista de sinais contenha nomes de sinais invalidos.
    """

    signals: set[str] = {"wind_speed", "power", "ambient_temperature"}

    @field_validator("signals")
    @classmethod
    def allowed_signals(cls, value: list[str] | None) -> set[str]:
        """Validar valores permitidos para os sinais usados na rota.

        Args:
            value (list[str] | None): Lista de sinais requisitados.

        Raises:
            ValidationError: Caso a lista de sinais contenha sinais inesperados.

        Returns:
            set[str]: Set com os sinais válidos.
        """
        allowed = {"wind_speed", "power", "ambient_temperature"}
        if not value:
            return allowed

        invalid = set(value) - allowed
        if invalid:
            msg = f"Invalid signal names given: {", ".join(invalid)}"
            raise ValidationError(msg)
        return set(value)

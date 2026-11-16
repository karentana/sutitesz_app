class CalculadoraViewModel:
    @staticmethod
    def calcular_puntos_antiguedad(anios_base, anios_empresa):
        if anios_base < 0 or anios_empresa < 0:
            raise ValueError("Los años de antigüedad no pueden ser negativos.")
        return (anios_base + anios_empresa) * 5

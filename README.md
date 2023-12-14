# CONTROL FINANCE EASY

Esta é uma API pensada para o controle financeiro de uma pessoa (CPF), onde o objetivo é facilitar a vida financeira, permitindo que você esteja ciente de tudo o que está entrando e saindo do seu bolso.

## Comandos CLI personalizado

- `python manage.py populate <nome_arquivo.csv> <type>` - Crie uma pasta chamada ***package_csv*** (obrigatoriamente esse nome) e jogue seu arquivo **CSV**. Definido o nome basta adiciona-lo ao final do comando não precisa do **.csv**, o próximo parâmetro é para definir se o CSV é relacionado a fatura de crédito ou da conta em geral temos duas opções (**credit** ou **others**). EX: `python manage.py populate NU_NOV_2023 others` (Funciona apenas para csv gerado pelo Nubank).

## DER

[Link referência](https://dbdiagram.io/d/Controll-Easy-Finance-60e0e40f0b1d8a6d39657fc5)
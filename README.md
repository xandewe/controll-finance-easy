# CONTROL FINANCE EASY

Esta é uma API pensada para o controle financeiro de uma pessoa (CPF), onde o objetivo é facilitar a vida financeira, permitindo que você esteja ciente de tudo o que está entrando e saindo do seu bolso. Para ajudar no entendimento da API aqui está o link para o DER [link referência](https://dbdiagram.io/d/Controll-Easy-Finance-60e0e40f0b1d8a6d39657fc5).

## Documentação

A documentação completa da API Controll Finance Easy está disponível no endpoint `api/schema/swagger/`. Este documento fornece uma visão geral rápida dos principais recursos, parâmetros de solicitação, respostas e exemplos práticos.

## Tecnologias utilizadas

- Python
- Django
- DRF (Django rest framework)
- Drf-spectacular
- Django-filter
- Ferramenta para manipulção de CSV
- Psycopg2-binary
- Djangorestframework-simplejwt

## Instalação

Certifique-se de ter o Python e as dependências necessárias instaladas. Você pode instalar as dependências usando o seguinte comando:

```bash
pip install -r requirements.txt
```

## Comandos CLI personalizado

- `python manage.py populate <nome_arquivo.csv> <type>` - Crie uma pasta chamada ***package_csv*** (obrigatoriamente esse nome) e jogue seu arquivo **CSV**. Definido o nome basta adiciona-lo ao final do comando não precisa do **.csv**, o próximo parâmetro é para definir se o CSV é relacionado a fatura de crédito ou da conta em geral temos duas opções (**credit** ou **others**). EX: `python manage.py populate NU_NOV_2023 others` (Funciona apenas para csv gerado pelo Nubank).

> [!IMPORTANT]
> Caso a opção do tipo seja o ***credit*** o nome do arquivo deve nesse formato ***nubank-ano-mes***. EX: `python manage.py populate nubank-2023-01 credit`

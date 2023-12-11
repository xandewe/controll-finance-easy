from django.core.management.base import BaseCommand, CommandError
from transactions.models import Transaction
import csv
import os
from decimal import Decimal


class Command(BaseCommand):
    help = "read csv to populate the DB"

    def add_arguments(self, parser):
        parser.add_argument("file_csv")

    def handle(self, *args, **options):
        file_csv = os.path.join("./package_csv", options["file_csv"])

        counter = 0

        if os.path.exists(file_csv):
            with open(file_csv, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for line in reader:
                    if reader.line_num > 1:
                        fields = ["created_at", "value", "name"]
                        line.pop(2)
                        data = dict(zip(fields, line))
                        data["value"] = Decimal(data["value"])
                        data["created_at"] = "-".join(
                            data["created_at"].split("/")[::-1]
                        )

                        if data["value"] < 0:
                            data.update({"category": "Expense"})
                            data["value"] = -1 * data["value"]
                        else:
                            data.update({"category": "Income"})

                        data.update({"status": "Done"})

                        Transaction.objects.create(**data)

                        counter += 1

                        self.stdout.write(self.style.SUCCESS(f"Processando ..."))

                self.stdout.write(
                    self.style.SUCCESS(
                        f"{counter} dados processados para o DB com sucesso"
                    )
                )

        else:
            self.stdout.write(
                self.style.ERROR(f"Arquivo não encontrado no diretório | {file_csv}")
            )

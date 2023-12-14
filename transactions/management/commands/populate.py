from django.core.management.base import BaseCommand, CommandError
from transactions.models import Transaction
import csv
import os
from decimal import Decimal


class Command(BaseCommand):
    help = "read csv to populate the DB"

    def add_arguments(self, parser):
        parser.add_argument("file_csv")
        parser.add_argument("is_credit", default="others", choices=("credit", "others"))

    def handle(self, *args, **options):
        file_csv = options["file_csv"].split(".")[0]
        file_path = os.path.join("./package_csv", f"{file_csv}.csv")
        is_credit = options["is_credit"]

        counter = 0

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)

                for line in reader:
                    if reader.line_num > 1:
                        if is_credit == "others":
                            fields = ["created_at", "value", "name"]
                            line.pop(2)
                            data = dict(zip(fields, line))
                            data["value"] = Decimal(data["value"])
                            data["created_at"] = "-".join(
                                data["created_at"].split("/")[::-1]
                            )

                            if data["value"] < 0:
                                data.update({"type": "Expense"})
                                data["value"] = -1 * data["value"]

                            else:
                                data.update({"type": "Income"})

                            data.update({"status": "Done"})

                            Transaction.objects.create(**data)

                        else:
                            if line[1] != "payment":
                                fields = ["description", "name", "value"]
                                date_purchase = line.pop(0)

                                data = dict(zip(fields, line))
                                data["value"] = Decimal(data["value"])
                                data.update(
                                    {
                                        "description": f'{date_purchase} {data["description"]}'
                                    }
                                )
                                data.update({"type": "Credit Card"})
                                data.update({"status": "Done"})
                                _, year, month = file_csv.split("-")
                                data.update({"created_at": f"{year}-{month}-01"})

                                Transaction.objects.create(**data)

                        self.stdout.write(self.style.SUCCESS(f"Processando ..."))
                        counter += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"{counter} dados processados para o DB com sucesso"
                    )
                )

        else:
            self.stdout.write(
                self.style.ERROR(f"Arquivo não encontrado no diretório | {file_path}")
            )

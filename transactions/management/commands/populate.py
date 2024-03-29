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
        counter_payment = 0

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

                            year_month_reference = data["created_at"][:-3]

                            data.update({"status": "Done", "year_month_reference": year_month_reference})

                            Transaction.objects.create(**data)

                            counter += 1

                        else:
                            if line[1] != "payment":
                                fields = ["created_at", "description", "name", "value"]

                                data = dict(zip(fields, line))
                                
                                data["value"] = Decimal(data["value"])
                                data.update({"type": "Credit Card"})
                                data.update({"status": "Done"})

                                _, year, month = file_csv.split("-")
                                data.update({"year_month_reference": f"{year}-{month}"})

                                Transaction.objects.create(**data)

                                counter += 1

                            else:
                                counter_payment += 1
                                
                        self.stdout.write(self.style.WARNING(f"Processando ..."))

                if is_credit == "others":
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"\n{counter} dados processados para o DB com sucesso"
                        )
                    )

                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"\n{counter+counter_payment} dados processados para o DB com sucesso\n{counter_payment} dados de pagamento\n{counter} dados de saída"
                        )
                    )

        else:
            self.stdout.write(
                self.style.ERROR(f"Arquivo não encontrado no diretório | {file_path}")
            )

"""
Dataset Generator
"""

from generators.ticket_generator import TicketGenerator
from generators.dataset_exporter import DatasetExporter
from utils.validator import TicketValidator

NUM_TICKETS = 1000   # We'll change to 100000 later


def main():

    generator = TicketGenerator()

    exporter = DatasetExporter()

    tickets = []

    print("Generating dataset...\n")

    for _ in range(NUM_TICKETS):

        ticket = generator.generate_ticket()

        if TicketValidator.validate(ticket):

            tickets.append(ticket)

    exporter.export(tickets)


if __name__ == "__main__":
    main()
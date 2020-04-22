from pdf import TinkoffPdfReport

def main():
    t = TinkoffPdfReport('out-inc-state-2019.pdf')
    payments = t.parse()
    for p in payments:
        p.print()


if __name__ == '__main__':
    main()
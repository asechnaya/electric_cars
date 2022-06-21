from pdf_generation import create_pdf
from plots import create_graph


def plot_graph():
    print("Enter two currencies: \n"
          "First currency = ")
    print("Second currency = ")


if __name__ == '__main__':
    image_path = 'currencies.png'
    currency_1 = 'gel'
    currency_2 = 'rub'
    create_graph(currency_1, currency_2)
    create_pdf(image_path, currency_1, currency_2)



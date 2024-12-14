import cbpro
import num2words
import string


def make_symbol_database_friendly(symbol):
    output = ''
    for letter in symbol:
        try:
            number = int(letter)
            word_equivalent = num2words.num2words(number)
            output = output + word_equivalent
        except:
            output = output + letter

    for i in string.punctuation:
        output = output.replace(i, '_')

    return output


client = cbpro.PublicClient()
all_currencies = {i['id']:i['name'] for i in client.get_currencies()}

curr_list = client.get_products()
usd_list = [i['id'] for i in curr_list if i['quote_currency'] == 'USD']

currencies = {}
for cur_pair in usd_list:
    currencies[cur_pair] = {}
    currencies[cur_pair]['database'] = make_symbol_database_friendly(cur_pair)
    currencies[cur_pair]['currency_pair'] = cur_pair
    currencies[cur_pair]['currency_name'] = all_currencies[cur_pair.split('-')[0]]

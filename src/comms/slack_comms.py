import sys
sys.path.insert(0, '../../../')
import requests
from sven.src.credentials import slack_credentials


class SlackCommunicator:

	def __init__(self):
		self.credentials = slack_credentials

	def check_trade_statuses(self):
		pass

	@staticmethod
	def format_df(df, top=10):
		periods = sorted([int(i.split('_')[1]) for i in df.columns if 'total' in i and 'all' not in i])
		all_data = []
		for idx, data_row in df.head(top).iterrows():
			entry = [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": """
:large_blue_circle:[Rank {}] *Stock Name: {}*
{}
:chart_with_upwards_trend: *Flagged Indicators* [{} day period - Total: {}]:
{}
{}
:chart_with_upwards_trend: *Flagged Indicators* [{} day period - Total: {}]:
{}
{}
:information_source:*Ratio [{}:{}]* - {}\n""".format(
							idx + 1,
							data_row['symbol'],
							'-' * 10,
							periods[0],
							data_row['total_' + str(periods[0])],
							'\n'.join(list(
								i for i in [j for j in data_row.index if str(periods[0]) in j and 'total' not in j] if
								data_row[i] > 0)),
							'-' * 10,
							periods[1],
							data_row['total_' + str(periods[1])],
							'\n'.join(list(
								i for i in [j for j in data_row.index if str(periods[1]) in j and 'total' not in j] if
								data_row[i] > 0)),
							'-' * 10,
							periods[0],
							periods[1],
							round(data_row['recency_ratio'], 4)
						)
					}
				},
				{"type": "divider"}
			]
			all_data += entry
		return all_data

	def post(self, webhook_url, df):
		webhook_url = webhook_url
		message = self.format_df(df)

		all_data = self.format_df(df)

		slack_data = {
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "plain_text",
						"text": "Sven Here! Check out the Latest Buy Options [{}]:".format(df.run_date.max()),
						"emoji": True
					}
				},
				{
					"type": "divider"
				},

				] + all_data + [

				{
					"type": "divider"
				}
			]
		}

		header = {'Content-Type': 'application/json'}
		response = requests.post(webhook_url, json=slack_data, headers=header)
		if response.status_code != 200:
			raise ValueError(
				'Request to slack returned an error %s, the response is:\n%s'
				% (response.status_code, response.text)
			)
		pass

	def confirm_finish(self):

		webhook_url = self.credentials['webhooks']['trading']


		slack_data = {
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "plain_text",
						"text": "Data Has finished updating...",
						"emoji": True
					}
				},
				{
					"type": "divider"
				},

			]
		}

		header = {'Content-Type': 'application/json'}
		response = requests.post(webhook_url, json=slack_data, headers=header)
		if response.status_code != 200:
			raise ValueError(
				'Request to slack returned an error %s, the response is:\n%s'
				% (response.status_code, response.text)
			)
		pass


if __name__=='__main__':

	slack_communicator = SlackCommunicator()

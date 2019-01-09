import pandas as pd

from driver_config import FlaurologicalDriver


class FlaurologicalDataStructure:

    def __init__(self, url):
        driver = FlaurologicalDriver()
        driver.run(url)
        driver.quit()

        self.data = []
        self.df = None

        self.preprocess_data(driver.data)
        self.save()

    def preprocess_data(self, old_data):
        session_title = ''
        title = ''
        for d in old_data:
            if 'session' in d['session-title'].lower():
                title = ''
                session_title = d['session-title']
            else:
                title = d['session-title']
            for i in range(len(d['speakerDetails']['names'])):
                self.data.append(self._gen_data(d, speaker_index=i, session_title=session_title, title=title))
        self._data_to_dataframe()
        print(self.data)

    def save(self):
        self.df.to_csv('data/flaurologicaldataset.csv')

    def _gen_data(self, d, *args, **kwargs):
        new_data = {}
        new_data['Session Title'] = kwargs['session_title']
        new_data['Title'] = kwargs['title']

        new_data['Position'] = d['speakerType'].strip(':').strip('s')  # Example: 'Speakers:'
        name = d['speakerDetails']['names'][kwargs['speaker_index']]
        name = name[:name.find(',')]
        name = name.split(' ')
        new_data['First Name'] = name[0]
        if len(name) > 2:
            new_data['Middle Name'] = name[1].strip('.')
        else:
            new_data['Middle Name'] = ''
        new_data['Last Name'] = name[-1]
        new_data['Workplace'] = d['speakerDetails']['Workplaces'][kwargs['speaker_index']]
        return new_data

    def _data_to_dataframe(self):
        self.df = pd.DataFrame(self.data)

from utils import *

format_list = ['Audio CD', 'VHS Tape', 'Amazon Video', 'Blu-ray', 'DVD', '3D', '4K', 'Multi-Format', 'Prime Video']

key_list = ['ASIN', 'Actors', 'Director', 'Format',
                    'Genres', 'Language', 'Rated',
                    'Region', 'Studio', 'Supporting actors',
                    'Writers', 'imdb', 'img']

# IMPORTANT change this directly to your json data file
path_dir = '/Users/Licor/Desktop/pagedata/'


files = glob.iglob(r'{}/*.[Jj]son'.format(path_dir))

content_list = []
# count = 0
csv_count = 0
for file in files:
    # count += 1
    # if count > 10:
    #     break
    with open(file, 'r') as f:
        content = json.load(f)
        if 'ASIN:' not in content:
            content['ASIN'] = file.title().split('/')[-1].split('.')[0]
        content_list.append(format_json(content, key_list, format_list))

        if not os.path.exists(path_dir + 'done/'):
            os.mkdir(path_dir + 'done/')
        shutil.move(file, path_dir + 'done/')

        if len(content_list) % 5000 == 0:
            print("finish 5000 lines!")

        # if len(content_list) > 10000:
        #     df = pd.DataFrame(content_list)
        #     if not os.path.exists(path_dir + 'csv/'):
        #         os.mkdir(path_dir + 'csv/')
        #     df.to_csv(path_dir + '{}.csv'.format(csv_count))
        #     csv_count += 1
        #     content_list = []

# save the rest
df = pd.DataFrame(content_list)
if not os.path.exists(path_dir + 'csv/'):
    os.mkdir(path_dir + 'csv/')
# df.to_csv(path_dir + 'csv/{}.csv'.format(csv_count))
df.to_csv(path_dir + 'csv/{}.csv'.format('output'))
print("finish all! total:{} lines.".format(len(content_list)))
content_list = []
import sys, os, datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords


def process_cloud(input_text ,genre):
    NUMBER_OF_GENRE = 8
    genres = ['Business', 'Education', 'Entertainment', 'Health', 'Medical', 'Sports', 'Technology', 'Others']
    fonts = [
        'Gloucester-MT-Extra-Condensed.ttf',
        'Cooper-Black.ttf',
        'Harlow-Solid-Italic.ttf',
        'Broadway.ttf',
        'Brush-Script-MT-Italic.ttf',
        'Gill-Sans-Ultra-Bold.ttf',
        'CopperplateGothicBold.ttf',
        'Wide-Latin.ttf',
    ] # genre[i] goes with fonts[i]

    #if len(sys.argv) == 4:
        # Usage: python3 word_cloud.py output_image_name genre_classified_by_model input_text
        # Example: python -u word_cloud.py "output_img" "Medical" "abcdefg..." # If no space, double quotes can be reduced
     #   fig_name = sys.argv[1]
      #  genre = sys.argv[2]
       # input_text = sys.argv[3]
    
    fig_name = genre
    for i in range(NUMBER_OF_GENRE):
        if genre == genres[i]:
            idx = i
            break
    font_path = os.getcwd() + "\\static\\assets\\" + fonts[i]
    background_image_path = os.getcwd() + "\\static\\assets\\" + genres[i] + ".JPG"
    
    nltk_stopwords = stopwords.words('english')
    customized_stopwords = ["the","and","i", "'s", "-", "--", "---", "n't", "'in", "``", "`", "'", "''", "'ll", "'ve"]
    Stopwords = customized_stopwords + nltk_stopwords + list(STOPWORDS)

    img = plt.imread(background_image_path)
    plt.figure('tmp', frameon = False, facecolor=(0, 0, 0, 0), edgecolor=(0, 0, 0, 0))
    plt.imshow(img)
    plt.margins(x = 0, y = 0)
    plt.xticks([])
    plt.yticks([])
    cloud(input_text, Stopwords, font_path)
    PATH = os.getcwd() + "\\static\\cloud_result\\"
    current_time = str(datetime.datetime.now()).split(" ")[1].replace(":", "-").replace(".", "-") # 2020-04-20 23:57:44.019598
    fig_name = fig_name + current_time
    plt.savefig(os.path.join(PATH, fig_name)) # Save to same folder as this python file
    fig_name = 'cloud_result/' + fig_name +'.png'

    return fig_name, font_path

def cloud(text, Stopwords, font_path):
    word = WordCloud(stopwords = Stopwords, width = 2000, height = 1500,\
                     font_path = font_path, min_font_size = 3, max_font_size = 400, max_words = 70,\
                     background_color = "rgba(255, 255, 255, 0)", mode = 'RGBA', colormap = plt.get_cmap('nipy_spectral') # nipy_spectral, tab10
           ).generate(text)
    plt.imshow( word, cmap = plt.get_cmap('jet'), alpha = 0.8)

## ----------------------------------------------------------------------------------------------------------------------------------- ##
# For testing
# current_time = str(datetime.datetime.now()).split(" ")[1].replace(":", "-").replace(".", "-") # 2020-04-20 23:57:44.019598 -> 23-57-44-019598
# fig_name = "tmp_" + current_time
# genre = "Business"
# input_text = '''A Star Is Born is a 2018 American musical romantic drama film produced and directed by \
# Bradley Cooper (in his directorial debut) and written by Eric Roth, Cooper and Will Fetters. A remake \
# of the 1937 film of the same name, it stars Cooper, Lady Gaga, Andrew Dice Clay, Dave Chappelle, and Sam \
# Elliott, and follows a hard-drinking musician (Cooper) who discovers and falls in love with a young singer \
# (Gaga). It marks the fourth remake of the original 1937 film, after the 1954 musical, the 1976 rock musical \
# and the 2013 Bollywood romance film. Talks of a remake of A Star Is Born began in 2011, with Clint Eastwood \
# attached to direct and Beyoncé set to star. The film was in development hell for several years with various \
# actors approached to co-star, including Christian Bale, Leonardo DiCaprio, Will Smith, and Tom Cruise. In March \
# 2016, Cooper signed on to star and direct, and Lady Gaga joined the cast in August 2016. Principal photography \
# began at the Coachella Valley Music and Arts Festival in April 2017.A Star Is Born premiered at the 75th Venice \
# International Film Festival on August 31, 2018, and was theatrically released in the United States on October 5, \
# 2018, by Warner Bros. The film has grossed over $260 million worldwide and received critical acclaim, with praise \
# for Cooper, Gaga and Elliott's performances and Cooper's direction, as well as the screenplay, cinematography and music.'''
## ----------------------------------------------------------------------------------------------------------------------------------- ##

    #if len(sys.argv) == 4:
        # Usage: python3 word_cloud.py output_image_name genre_classified_by_model input_text
        # Example: python -u word_cloud.py "output_img" "Medical" "abcdefg..." # If no space, double quotes can be reduced
        #fig_name = sys.argv[1]
        #genre = sys.argv[2]
        #input_text = sys.argv[3]
    
# plt.show()

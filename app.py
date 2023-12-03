# app.py
import pandas as pd
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

def classify_sentiment(rating):
    if rating >= 4:
        return 'Positive'
    else:
        return 'Negative'

def analyze_comments(df):
    # Separate positive and negative comments
    positive_comments = df[df['Sentiment'] == 'Positive']['Comment'].astype(str)
    negative_comments = df[df['Sentiment'] == 'Negative']['Comment'].astype(str)

    # Count the occurrences of words in positive comments
    positive_word_counts = Counter(" ".join(positive_comments).split())

    # Count the occurrences of words in negative comments
    negative_word_counts = Counter(" ".join(negative_comments).split())

    # Display the counts
    positive_count = len(positive_comments)
    negative_count = len(negative_comments)

    # Display the most common words in positive comments
    most_common_positive = positive_word_counts.most_common(10)

    # Display the most common words in negative comments
    most_common_negative = negative_word_counts.most_common(10)

    return positive_count, negative_count, most_common_positive, most_common_negative

def generate_word_cloud(word_counts, filename):
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.title(filename)
    plt.savefig(f'static/{filename}.png')  # Save word cloud image
    plt.close()

@app.route('/')
def index():
    # Load the Data with specific columns and using semicolon as the delimiter
    df = pd.read_csv('data/ReviewPVJ.csv', usecols=['Rating', 'Comment'], delimiter=';')

    # Apply Sentiment Analysis
    df['Sentiment'] = df['Rating'].apply(classify_sentiment)

    # Optional - Analyze Comment Sentiment
    positive_count, negative_count, most_common_positive, most_common_negative = analyze_comments(df)

    # Optional - Save the Result
    df.to_csv('data/output_file.csv', index=False)

    # Generate word clouds
    generate_word_cloud(Counter(" ".join(df['Comment']).split()), 'wordcloud')
    generate_word_cloud(Counter(" ".join(df[df['Sentiment'] == 'Positive']['Comment']).split()), 'wordcloud_positive')
    generate_word_cloud(Counter(" ".join(df[df['Sentiment'] == 'Negative']['Comment']).split()), 'wordcloud_negative')

    return render_template('index.html',
                           positive_count=positive_count,
                           negative_count=negative_count,
                           most_common_positive=most_common_positive,
                           most_common_negative=most_common_negative)

if __name__ == '__main__':
    app.run(debug=True)

#this function will take as input a list of word and reutrn a string of the most occured word


def find_most_frequent_word(word_list):
    
    word_counts = {}  # Dictionary to store word counts
    # Count the occurrences of each word
    for word in word_list:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
            
    # Find the most frequent word
    if len(word_counts)>0:
        most_frequent_word = max(word_counts, key=word_counts.get)
        return most_frequent_word

########################################################################################################


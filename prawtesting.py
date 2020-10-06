import praw
import sys, getopt

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

def processCommand(argv):
    arguments = dict()
    try:
        opts, args = getopt.getopt(argv,"hr:o:",["subreddit=","ofile="])
    except getopt.GetoptError:
        print ('prawtesting.py -r <subreddit> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('prawtesting.py -r <subreddit> -o <outputfile>')
            sys.exit()
        elif opt in ("-r", "--subreddit"):
            arguments['subredditname'] = arg
        elif opt in ("-o", "--ofile"):
            arguments['outputfile'] = arg
    print ('Output file is:', arguments['outputfile'])
    print ('Subreddit is:', arguments['subredditname'])
    return arguments

#30 api calls per minute

def apiCall(argv):
    reddit = praw.Reddit(client_id = '',
                        client_secret = '',
                        username = '',
                        password = '',
                        user_agent = '')

    subreddit = reddit.subreddit(argv['subredditname'])

    top_soundblasterofficial = subreddit.top("day")
    with open(argv['outputfile'], 'w+') as fout:
        for submission in top_soundblasterofficial:
            print(20*'-')
        #             print('Parent ID:', comment.parent())
        #             print('Comment ID:', comment.id)
            print('Title: {}, Ups: {}, Downs: {}, Have we visited: {}'.format(submission.title,
                                                                            submission.ups,
                                                                            submission.downs,
                                                                            submission.visited))
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                print(comment.body)
                fout.write(comment.body)
    #for comment in subreddit.stream.comments():
    fout.close()

if __name__ == "__main__":
    arguments = processCommand(sys.argv[1:])
    print(arguments)
    apiCall(arguments)

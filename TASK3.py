import random
from flask import flask, jsonify
app =flask(__name__)
fortynes =[
    "you will have a plesant surprise.",
    "A thrilling time is in your near future.",
    "Someone is thinking of you right now.",
    "You will find great success in your next endeavor.",
    "Now is the time to try something new.",
]
jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
"Why don't programmers like nature? It has too many bugs.",
    "What do you get when you cross a snowman and a vampire? Frostbite.",
    "I would tell you a joke about an elevator, but it's an uplifting experience."
]
facts = [
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
    "A group of flamingos is called a 'flamboyance'.",
    "Bananas are berries, but strawberries are not.",
    "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of metal in the heat.",
    "Octopuses have three hearts!"
]
@app.route('/fortune')
def fortune():
    return jsonify(message=random.choice(fortunes))

@app.route('/joke')
def joke():
    return jsonify(message=random.choice(jokes))

@app.route('/fact')
def fact():
    return jsonify(message=random.choice(facts))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
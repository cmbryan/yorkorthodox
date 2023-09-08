from .test_util import client


def test_root_response(client):
    response = client.get("/")
    assert b"<h1>yorkorthodox.org REST service</h1>" in response.data


def test_lectionary(client):
    """Check the full content of a 'typical' day"""
    response = client.get("/lectionary", query_string={"date": "2023-01-01"})
    assert response.json == {
        "basil": "Liturgy of St Basil",
        "british_saints": "St. Maelrhys of the Isle of Bardsey (6th C). SS Elvan and "
        "Mydwyn, missionaries of Britain (2nd C). St. Beoc, abbot "
        "of Lough Derg (5th C). St. Connat, abbess of Kildare "
        "(590). St. Cuan (6th C). St. Fanchea, abbess of Rossory "
        "(585). St. Ernan mac Eoghan (c.640).\n",
        "date_str": "Sunday, 1st January 2023",
        "desig": "29th after Pentecost, 15th of Luke, The Circumcision of our Lord "
        "and Saviour Jesus Christ, St. Basil the Great, Archbishop of "
        "Cæsarea in Cappadocia (379)",
        "fast": None,
        "general_saints": "St. Gregory, bishop of Nazianzus, father of St. Gregory "
        "the Theologian (4th C). Holy martyr Basil of Ancyra (362). "
        "New martyr Peter of The Peloponnese. Holy martyr "
        "Theodotos. St. Theodosius of Tryglia, abbot. St. Almachius "
        "(391). St. Fulgentius, bishop of Ruspe in North Africa "
        "(533).",
        "tone": "Tone 4 - Eothinon 7",
        "a_lect_1": "Colossians 3:4-11",
        "a_lect_2": None,
        "a_text_1": "<em>Colossians 3:4-11</em><br>When Christ, our life, is "
        "revealed, then we too shall be revealed with him in glory. Put "
        "to death then the parts of you that are of the earth: sexual "
        "immorality, impurity, lust, depraved desire, and greed which is "
        "idolatry. The wrath of God is coming upon the children of "
        "disobedience because of these things with which you also once "
        "occupied yourselves when you were living among them. But now rid "
        "yourselves of them all: anger, hot-headedness, malice, "
        "blasphemy, foul language from your mouth. Do not lie to one "
        "another. You have put off the old self with its practices, and "
        "you have put on the new which is being restored in "
        "understanding, in accordance with the image of him who created "
        "it, where there is no Greek and Jew, circumcision and "
        "uncircumcision, barbarian, Scythian, slave and free, but Christ "
        "is all, and is in all.<br><br>",
        "a_text_2": "",
        "c_lect_1": "<b>Colossians 2:8-12</b>",
        "c_lect_2": "<b>Luke 2:20-21, 40-52</b>",
        "c_text_1": "<em>Colossians 2:8-12</em><br>See that no one carries you away "
        "with philosophy and empty delusion according to human tradition "
        "and the elemental principles of the world and not according to "
        "Christ. For in him resides all the fullness of the divine nature "
        "in bodily form. And in him, who is the head of all rule and "
        "authority, you are fulfilled. And in him you have been "
        "circumcised with a circumcision not performed by human hand, "
        "through the casting off of the sinful body of flesh in the "
        "circumcision of Christ. You have been buried with him in "
        "baptism, in which you were also raised with him through faith by "
        "the working of God who raised him from the dead.<br><br>",
        "c_text_2": "<em>Luke 2:20-21, 40-52</em><br>Then the shepherds returned, "
        "glorifying and praising God for all that they had heard and "
        "seen, just as it had been told to them. When the eight days had "
        "passed for the child to be circumcised, he was named Jesus, "
        "having been given that name by the angel before he was conceived "
        "in the womb. … The child grew and became strong in spirit, full "
        "of wisdom, and the grace of God was upon him. Now each year his "
        "parents would make the journey to Jerusalem for the feast of the "
        "Passover, and when he was twelve years old they went up to "
        "Jerusalem for the feast, as was the custom. The days passed, and "
        "on their return the boy Jesus stayed behind in Jerusalem, but "
        "his mother and Joseph did not know. Supposing him to be in the "
        "company, they went a day’s journey and then began looking for "
        "him among their relatives and acquaintances. When they did not "
        "find him, they turned back to Jerusalem to look for him. It was "
        "three days later that they found him in the Temple, sitting "
        "among the teachers, listening to them and asking them questions. "
        "All who heard him were astonished by his intellect and his "
        "responses. When they saw him they were astounded, and his mother "
        "said to him, ‘Son, why have you done this to us? Your father and "
        "I have been anxiously looking for you.’ He asked them, ‘Why were "
        "you looking for me? Did you not realise that I had to be about "
        "my Father’s business?’ But they did not understand what he was "
        "saying to them. Then he went down with them and came to "
        "Nazareth, and he was obedient to them. His mother remembered in "
        "her heart all that was said. And Jesus grew in wisdom and in "
        "stature, and in favour with God and with people.<br><br>",
        "date_str": "Sunday, 1st January 2023",
        "desig": "29th after Pentecost, 15th of Luke, The Circumcision of our Lord "
        "and Saviour Jesus Christ, St. Basil the Great, Archbishop of "
        "Cæsarea in Cappadocia (379)",
        "fast": None,
        "g_lect": "Luke 19:1-10",
        "g_text": "<em>Luke 19:1-10</em><br>He entered Jericho, and was passing "
        "through when a man called Zacchaeus appeared. He was a chief tax "
        "collector, and rich. He wanted to catch sight of Jesus, to see who "
        "he was, but being small in stature he could not because of the "
        "crowd. He ran on ahead and climbed a sycamore tree in order to see "
        "him, because he was about to pass by. When Jesus reached the "
        "place, he looked up and saw him and said to him, ‘Zacchaeus, come "
        "down quickly. Today I must stay at your house.’ He hurried down "
        "and welcomed him joyfully. But when they saw this they grumbled, "
        "saying, ‘He has gone to stay with a sinful man.’ Zacchaeus stood "
        "there and said to the Lord, ‘Listen, Lord. I am giving half of "
        "what belongs to me to the poor, and if I have defrauded anyone of "
        "anything, I shall repay it four times over.’ And Jesus said of "
        "him, ‘Today salvation has come to this house, because he too is a "
        "son of Abraham. For the Son of Man has come to seek and to save "
        "the lost.’<br><br>",
        "x_lect_1": "",
        "x_lect_2": "",
        "x_text_1": "",
        "x_text_2": "",
    }


def test_no_liturgy_days(client):
    """Test that the readings for the Liturgy are not bolded during Lent, or Wed/Fri of Cheesefare week"""
    for date in [
        "2023-02-22",  # Cheesefare Wed
        "2023-02-24",  # Cheesefare Fri
        "2023-02-27",  # Clean Mon
    ]:
        response = client.get("/lectionary", query_string={"date": date})
        for lect in ["a_lect_1", "a_lect_2", "g_lect", "c_lect_1", "c_lect_2", "x_lect_1", "x_lect_2"]:
            if response.json[lect]:
                assert "<b>" not in response.json[lect]

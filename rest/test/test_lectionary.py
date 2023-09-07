from .test_util import client


def test_root_response(client):
    response = client.get("/")
    assert b"<h1>yorkorthodox.org REST service</h1>" in response.data


def test_lectionary(client):
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
    }

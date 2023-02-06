from events.Event import Event
class LocationEvent(Event):

    def getData(self, sender_id, reciever_id, args=None):
        data = dict()
        body = {
            "patient_id":sender_id,
            "location":args
        }
        data['user_id'] = reciever_id
        data['title'] = "Your patient has gone to a strange plce"
        data['type'] ="tes"
        data['body'] = body
from events.Event import Event


class PatientAgendaEvent(Event):

    def getData(self, sender_id, reciever_id, args=None):
        data = dict()
        data['user_id'] = reciever_id
        data['title'] = "قريبك مخدش الدوا"
        data['type'] = "important"
        data['body'] = {
            "content": "قريبك نسي ياخد الدوا",
            "agenda_id": args.agenda_id
        }

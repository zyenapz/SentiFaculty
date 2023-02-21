from feedback.models import Feedback
from datetime import date
from datetime import datetime, timedelta

from visualizer.models import Strand, FacultyEvaluation
from users.models import Teacher

class SF_CommentReport:
    def __init__(self, user_id, faculty_eval):

        query = Feedback.objects.filter(
            evaluatee__teacher__user__id=user_id, 
            evaluatee__fe=faculty_eval
        )
        feedbacks = list(query)

        self.comments_total = len(query)
        
        # Count comments today and this week
        self.comments_today = 0
        self.comments_thisweek = 0

        last_week = [datetime.today().date() - timedelta(days=i) for i in range(7)]

        for feedback in feedbacks:
            submit_date = feedback.submit_date.date()
            if submit_date == datetime.today().date():
                self.comments_today += 1

            if submit_date in last_week:
                self.comments_thisweek += 1

class SF_StrandReport:
    def __init__(self, user_id, faculty_eval):
        general_query = Feedback.objects.filter(
            evaluatee__teacher__user__id=user_id,
            evaluatee__fe=faculty_eval
        )

        # Query feedbacks by strand
        stem_query = list(general_query.filter(evaluator__strand__strand_name=Strand.StrandChoices.STEM))
        humss_query = list(general_query.filter(evaluator__strand__strand_name=Strand.StrandChoices.HUMSS))
        abm_query = list(general_query.filter(evaluator__strand__strand_name=Strand.StrandChoices.ABM))
        ict_query = list(general_query.filter(evaluator__strand__strand_name=Strand.StrandChoices.ICT))

        queries = {
            "stem": stem_query,
            "humss": humss_query, 
            "abm": abm_query, 
            "ict": ict_query,
        }

        # Tally sentiments by strand
        self.sentis = {
            "stem": {"positive": 0, "neutral": 0, "negative": 0, "total": 0,},
            "humss": {"positive": 0, "neutral": 0, "negative": 0, "total": 0,},
            "abm": {"positive": 0, "neutral": 0, "negative": 0, "total": 0,},
            "ict": {"positive": 0, "neutral": 0, "negative": 0, "total": 0,},
        }

        strands = ["stem", "humss", "abm", "ict"]
        for strand in strands:
            for feedback in queries[strand]:
                sentiment = feedback.comment.sentiment_score.get_sentiment_as_str()

                if sentiment == "positive":
                    self.sentis[strand]["positive"] += 1
                elif sentiment == "negative":
                    self.sentis[strand]["negative"] += 1
                else:
                    self.sentis[strand]["neutral"] += 1

                self.sentis[strand]["total"] += 1

        # Calculate and tally approval ratings by strand
        self.approval_rates = {
            "stem": 0,
            "humss": 0,
            "abm": 0,
            "ict": 0,
        }

        for strand in strands:
            pos = self.sentis[strand]["positive"]
            neg = self.sentis[strand]["negative"]
            total = self.sentis[strand]["total"]
            
            if total != 0:
                approval = ( (pos) / (pos+neg) ) * 100.0
                self.approval_rates[strand] = round(approval, 2)
            else:
                self.approval_rates[strand] = None

class SF_SubjectReport:
    def __init__(self, user_id, faculty_eval):
        query = Feedback.objects.filter(
            evaluatee__teacher__user__id=user_id,
            evaluatee__fe=faculty_eval
        )

        feedbacks = list(query)

        subjects = set([feedback.evaluatee.subject.subject_code for feedback in feedbacks])
        self.subjects_approval = {code: {"positive": 0, "negative": 0, "neutral": 0, "total": 0, "approval": 0} for code in subjects}

        for subject in self.subjects_approval:
            for feedback in feedbacks:
                if subject == feedback.evaluatee.subject.subject_code:
                    sentiment = feedback.comment.sentiment_score.get_sentiment_as_str()

                    if sentiment == "positive":
                        self.subjects_approval[subject]["positive"] += 1
                    elif sentiment == "negative":
                        self.subjects_approval[subject]["negative"] += 1
                    else:
                        self.subjects_approval[subject]["neutral"] += 1

                    self.subjects_approval[subject]["total"] += 1

            # Tally and calculate approval for subject
            pos = self.subjects_approval[subject]["positive"]
            neg = self.subjects_approval[subject]["negative"]
            total = self.subjects_approval[subject]["total"]
            
            if total != 0:
                approval = ( (pos) / (pos+neg) ) * 100.0
                self.subjects_approval[subject]["approval"] = round(approval, 2)
            else:
                self.subjects_approval[subject]["approval"] = None    

        pass

class SF_FacultyRankings:
    #prepares a sorted list of faculty members: 2d array with (name: index 0,averageScore: index 1)
    def __init__(self, faculty_eval=FacultyEvaluation.objects.filter(is_ongoing=True).first()):
        teachers=Teacher.objects.filter(evaluatee__fe=faculty_eval).distinct()
        self.teachersAveraged={}
        for teacher in teachers:
            feedbacks=Feedback.objects.filter(evaluatee__teacher__user__mcl_id=teacher.user.mcl_id)
            feedbackScores=[entry.comment.sentiment_score.hybrid_pos - entry.comment.sentiment_score.hybrid_neg for entry in feedbacks]
            feedbackAverage=sum(feedbackScores)/len(feedbackScores)
            self.teachersAveraged[str(teacher)]=[feedbackAverage, teacher.user.id]
        self.teachersSorted=sorted(self.teachersAveraged.items(), key=lambda x: x[1], reverse=True)
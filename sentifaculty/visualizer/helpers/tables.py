import django_tables2 as tables
from feedback.models import Feedback
from django_filters.views import FilterView
import django_filters
from visualizer.models import Section, Strand, YearLevel, Subject

class FeedbackTable(tables.Table):
    class Meta:
        model = Feedback
        fields = (
            "evaluatee.subject",
            "comment", 
            #"comment.sentiment_score.get_sentiment_as_str.upper",
            "comment.sentiment_score.get_hybrid_total",
            "evaluator.strand",
            "evaluator.year_level",
            "evaluator.section",
        )

        row_attrs = {
            "sentiment-label": lambda record: record.comment.sentiment_score.get_sentiment_as_str
        }

        template_name = "visualizer/sf_table.html"
        
class FeedbackFilterSet(django_filters.FilterSet):
    section = django_filters.ModelChoiceFilter(field_name="evaluator__section", queryset=Section.objects.all(), lookup_expr="exact", label="Sections")
    strand = django_filters.ModelChoiceFilter(field_name="evaluator__strand", queryset=Strand.objects.all(), lookup_expr="exact", label="Strands")
    year_level = django_filters.ModelChoiceFilter(field_name="evaluator__year_level", queryset=YearLevel.objects.all(), lookup_expr="exact", label="Year Levels")
    # subject = django_filters.ModelChoiceFilter(field_name="evaluator__subject", queryset=Subject.objects.all(), lookup_expr="exact", label="Subjects")
    # subject = django_filters.ModelChoiceFilter(field_name="comment__sentiment_score__get_hybrid_total", queryset=Subject.objects.all(), lookup_expr="exact", label="Subjects")

    class Meta:
        model = Feedback 
        fields = []
    #     fields = ['section', 'strand', 'year_level']

class FilteredFeedbackListView(tables.SingleTableMixin, FilterView):
    table_class = FeedbackTable 
    model = Feedback 

    filterset_class = FeedbackFilterSet
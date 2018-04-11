import json


from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView

from plag import const
from plag.models import ScanResult
from plag.services import process_homepage_trial, post_process_index_trial


class IndexView(TemplateView):
    template_name = 'plag/static/index.html'

    def get_context_data(self, **kwargs):
        return {'accepted_file_exts': const.ACCEPTED_FILE_EXTENSIONS}




@login_required
# TODO This excludes ones which haven't been post scanned. But the overall count does not. Also this doesn't look at false positives
def plagiarism_results(request, scan_id=-1):
    scan_results = ScanResult.objects.filter(result_log=scan_id,
                                             result_log__protected_resource__order__user=request.user,
                                             post_scanned=True)

    return_data = []
    for result in scan_results:
        return_data.append({
            'match_url': result.match_url,
            'match_display_url': result.match_display_url,
            'match_title': result.match_title,
            'match_desc': result.match_desc,
            'perc_of_duplication': str(result.perc_of_duplication),
        })

    return HttpResponse(json.dumps(return_data), content_type="application/json")


class IndexTrialView(View):
    template = 'plag/static/index_trial.html'

    def get(self, request, *args, **kwargs):
        scan_log_id = request.GET.get('id1')
        scan_result_id = request.GET.get('id2')
        result = post_process_index_trial(request, scan_log_id, scan_result_id)
        perc_dup = result.perc_of_duplication if result else -1

        return HttpResponse(json.dumps({'id': scan_result_id, 'perc_dup': perc_dup, }), content_type="application/json")

    def post(self, request, *args, **kwargs):
        results = process_homepage_trial(request)

        ctx = {
            'scan_log': results[0],
            'scan_results': results[1],
        }

        return render_to_response(self.template, ctx, context_instance=RequestContext(request))

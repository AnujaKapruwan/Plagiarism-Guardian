import os
import uuid
from django.conf import settings
from plag.management.commands import post_processing
from plag.models import ProtectedResource, ScanResult, ScanLog, Query
from util.getqueriespertype import url, txt, pdf, doc, docx, pptx
from util import handlequeries



def process_homepage_trial(request):

    scan_results = []
    param_url = request.POST.get('url')
    param_file = request.FILES.get('plagFile')

    if param_url:
        queries = url.get_queries(param_url)
    elif param_file:
        extension = os.path.splitext(param_file.name)[1][1:]
        extension = extension.upper() if extension is not None else ''

        if extension in [ProtectedResource.PDF, ProtectedResource.DOC,]:
            filename = get_unique_filename(extension)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            with open(file_path, 'wb') as dest:
                dest.write(param_file.read())

            if extension == ProtectedResource.PDF:
                queries = pdf.get_queries(filename)
            elif extension == ProtectedResource.DOC:
                queries = doc.get_queries(filename)

            os.remove(file_path)
        elif extension == ProtectedResource.DOCX:
            queries = docx.get_queries(param_file)
        elif extension == ProtectedResource.PPTX:
           queries = pptx.get_queries(param_file)
        else:
            queries = txt.get_queries(param_file.read().decode("utf-8"))

    # TODO Too similar to scan_resources code
    if queries['success']:
        log = ScanLog(protected_source=queries['source'], user_ip=get_client_ip(request))
        log.save()

        query_list = []
        for query in queries['data']:
            q = Query(query=query)
            q.save()
            query_list.append(q)

        log.queries.add(*query_list)
        log.save()

    if queries['success'] and len(queries['data']) > 0:
        results = handlequeries.run_request(queries['data'], [param_url, ])

        for result in results:
            scan_result = ScanResult(result_log=log, match_url=result['url'],
                                     match_display_url=result['displayurl'], match_title=result['title'],
                                     match_desc=result['desc'], post_scanned=False)
            scan_result.save()
            scan_results.append(scan_result)
    else:
        if queries['success'] and len(queries['data']) == 0:
            reason = 'No suitable content found'
            fail_type = ScanLog.C
        else:
            log = ScanLog(user_ip=get_client_ip(request))
            reason = queries['data']
            fail_type = ScanLog.H

        log.fail_reason = reason
        log.fail_type = fail_type
        log.save()

    return log, scan_results


def post_process_index_trial(request, scan_log_id, scan_result_id):
    user_ip = get_client_ip(request)
    result = ScanResult.objects.filter(pk=scan_result_id, result_log__pk=scan_log_id, result_log__user_ip=user_ip)

    if result:
        return post_processing.post_process_result(result[0])
    else:
        return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_unique_filename(extension):
    while True:
        filename = "%s.%s" % (uuid.uuid4(), extension)
        try_path = os.path.join(settings.MEDIA_ROOT, filename)

        if os.path.isfile(try_path):
            continue
        else:
            return filename


import urllib.request
from urllib.error import HTTPError, URLError
from socket import timeout
from plag.models import ScanLog
from util.textcleanup import html_to_basic_text, remove_special_characters, generate_ngrams


def post_process_result(result):
    # If the result is a PDF, Word doc or Powerpoint presentation, skip over it for now (TODO)
    if result.match_url.lower().endswith(('doc','docx','pdf')):
        result.perc_of_duplication = -1
        result.post_scanned = True
        result.save()
        return result

    # Firstly get the HTML for this API result (URL)
    try:
        url_result = urllib.request.urlopen(urllib.request.Request(result.match_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}),
                                            timeout=5).read()
    except (HTTPError, URLError) as e:
        result.perc_of_duplication = -1
        result.post_fail_reason = str(e)
        result.post_fail_type = ScanLog.H
        result.post_scanned = True
        result.save()
        return result
    except timeout as t:
        result.perc_of_duplication = -1
        result.post_fail_reason = 'URL timed out'
        result.post_fail_type = ScanLog.H
        result.post_scanned = True
        result.save()
        return result
    else:
        try:
            url_text = url_result.decode('utf-8')
        except UnicodeDecodeError:
            url_text = url_result.decode('ISO-8859-1')

        result_text = html_to_basic_text(url_text)
        queries_in_result = [query.query for query in result.result_log.queries.all() if
                             remove_special_characters(query.query) in result_text]

        # If no queries exist in the result, this must be a false positive - i.e. Bing has returned rubbish results
        if len(queries_in_result) == 0:
            result.perc_of_duplication = -1
            result.post_fail_reason = 'False positive'
            result.post_fail_type = ScanLog.C
        else:
            # Else the results seem okay, so work out a % duplication based on trigrams (NumMatchedTGs / NumProtectedTGs * 100)
            source_text = html_to_basic_text(result.result_log.protected_source)
            source_trigrams = generate_ngrams(source_text.lower())
            result_trigrams = generate_ngrams(result_text.lower())

            num_trigram_intersection = len(
                [source for source in source_trigrams if source.lower() in result_trigrams])
            result.perc_of_duplication = (num_trigram_intersection / len(source_trigrams)) * 100

        result.post_scanned = True
        result.save()
        return result
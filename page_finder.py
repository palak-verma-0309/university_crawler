from urllib.parse import urlparse
class PageFinder:
    ADMISSION_KEYWORDS = [
        "admission",
        "admissions",
        "apply"
    ]

    TUITION_KEYWORDS = [
        "tuition",
        "fees",
        "cost",
        "financial-aid"
    ]

    def _score_url(self, url, keywords):
        score = 0
        clean_url = url.lower().split("#")[0]
        for keyword in keywords:
            if keyword in clean_url:
                score += 10
        path = urlparse(clean_url).path
        depth = len([p for p in path.split("/") if p])
        score -= depth
        return score

    def get_top_candidates(self,urls,keywords,top_n=10):
        scored = []
        for url in urls:
            score = self._score_url(url,keywords)
            if score > 0:
                scored.append((score, url))
        scored.sort(key=lambda x: ( -x[0],len(x[1])))
        return scored[:top_n]

    def find_admissions_page(self, urls):
        candidates = self.get_top_candidates(urls,self.ADMISSION_KEYWORDS,top_n=1)
        return candidates[0][1] if candidates else None

    def find_tuition_page(self, urls):
        candidates = self.get_top_candidates(urls,self.TUITION_KEYWORDS,top_n=1)
        return candidates[0][1] if candidates else None
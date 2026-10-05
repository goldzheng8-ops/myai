from __future__ import annotations

from xml.etree.ElementTree import Element

from .xml import XmlFeedParser


class SitemapParser(XmlFeedParser):
    """Parse Sitemap and Sitemap Index."""

    def extract(
        self,
        *,
        root: Element,
        namespace: str,
    ) -> list[str]:

        match self._local_name(root.tag):

            case "urlset":
                return self._extract_urlset(
                    root,
                    namespace,
                )

            case "sitemapindex":
                return self._extract_index(
                    root,
                    namespace,
                )

            case _:
                raise ValueError(
                    f"Unsupported sitemap: {root.tag}"
                )

    def _extract_urlset(
        self,
        root: Element,
        namespace: str,
    ) -> list[str]:

        urls: list[str] = []

        for url in self._find_all(
            root,
            f"{namespace}url",
        ):

            self._append_text(
                urls,
                url,
                f"{namespace}loc",
            )

        return urls

    def _extract_index(
        self,
        root: Element,
        namespace: str,
    ) -> list[str]:

        urls: list[str] = []

        for sitemap in self._find_all(
            root,
            f"{namespace}sitemap",
        ):

            self._append_text(
                urls,
                sitemap,
                f"{namespace}loc",
            )

        return urls
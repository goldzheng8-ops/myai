from __future__ import annotations

from xml.etree.ElementTree import Element

from .xml import XmlFeedParser


class RssParser(XmlFeedParser):
    """Parse RSS 2.0 and Atom feeds."""

    def extract(
        self,
        *,
        root: Element,
        namespace: str,
    ) -> list[str]:

        match self._local_name(root.tag):

            case "rss":
                return self._extract_rss(root)

            case "feed":
                return self._extract_atom(
                    root,
                    namespace,
                )

            case _:
                raise ValueError(
                    f"Unsupported feed type: {root.tag}"
                )

    def _extract_rss(
        self,
        root: Element,
    ) -> list[str]:

        urls: list[str] = []

        channel = self._find(
            root,
            "channel",
        )

        if channel is None:
            return urls

        for item in self._find_all(
            channel,
            "item",
        ):

            self._append_text(
                urls,
                item,
                "link",
            )

        return urls

    def _extract_atom(
        self,
        root: Element,
        namespace: str,
    ) -> list[str]:

        urls: list[str] = []

        for entry in self._find_all(
            root,
            f"{namespace}entry",
        ):

            for link in self._find_all(
                entry,
                f"{namespace}link",
            ):

                self._append_attribute(
                    urls,
                    link,
                    "href",
                )

        return urls
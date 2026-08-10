from __future__ import annotations

from abc import abstractmethod

from defusedxml import ElementTree
from xml.etree.ElementTree import Element

from .base import FeedParser


class XmlFeedParser(FeedParser):

    def parse(
        self,
        content: str,
    ) -> list[str]:

        root = self._parse_xml(content)

        namespace = self._namespace(root)

        urls = self.extract(
            root=root,
            namespace=namespace,
        )

        return self._normalize(urls)

    @abstractmethod
    def extract(
        self,
        *,
        root: Element,
        namespace: str,
    ) -> list[str]:
        ...

    @staticmethod
    def _parse_xml(
        content: str,
    ) -> Element:

        try:
            return ElementTree.fromstring(content)

        except ElementTree.ParseError as exc:

            raise ValueError(
                "Invalid XML document."
            ) from exc

    @staticmethod
    def _namespace(
        node: Element,
    ) -> str:

        tag = node.tag

        if tag.startswith("{"):

            return tag.split(
                "}",
                1,
            )[0] + "}"

        return ""

    @staticmethod
    def _local_name(
        tag: str,
    ) -> str:

        if "}" in tag:

            return tag.split(
                "}",
                1,
            )[1]

        return tag

    @staticmethod
    def _find(
        node: Element,
        path: str,
    ) -> Element | None:

        return node.find(path)

    @staticmethod
    def _find_all(
        node: Element,
        path: str,
    ) -> list[Element]:

        return list(
            node.findall(path)
        )

    @classmethod
    def _find_text(
        cls,
        node: Element,
        path: str,
    ) -> str | None:

        element = cls._find(
            node,
            path,
        )

        if element is None:

            return None

        return cls._text(element)

    @staticmethod
    def _text(
        node: Element,
    ) -> str | None:

        if node.text is None:

            return None

        text = node.text.strip()

        return text or None

    @staticmethod
    def _attribute(
        node: Element,
        name: str,
    ) -> str | None:

        value = node.attrib.get(name)

        if value is None:

            return None

        value = value.strip()

        return value or None

    @classmethod
    def _append_text(
        cls,
        result: list[str],
        node: Element,
        path: str,
    ) -> None:

        text = cls._find_text(
            node,
            path,
        )

        if text:

            result.append(text)

    @classmethod
    def _append_attribute(
        cls,
        result: list[str],
        node: Element,
        name: str,
    ) -> None:

        value = cls._attribute(
            node,
            name,
        )

        if value:

            result.append(value)

    @staticmethod
    def _normalize(
        urls: list[str],
    ) -> list[str]:

        result: list[str] = []

        visited: set[str] = set()

        for url in urls:

            url = url.strip()

            if not url:

                continue

            if url in visited:

                continue

            visited.add(url)

            result.append(url)

        return result
## Simplewiki dataset
This directory provides cleaned and labeled dataset from [simplewiki][].
[simplewiki]: https://simple.wikipedia.org/

 
### Schema

Pages/Articles are formatted with one article per line. Each article has
following schema.
```json
{
  "id": "6",
  "url": "https://simple.wikipedia.org/wiki?curid=6",
  "title": "Art",
  "text": "Art description goes here",
  "categories": ["Non-verbal communication", "Basic English 850 words"]
}
```

### Source dumps

| Dataset type   | Source dump used | Latest dump link      |
|----------------|------------------|-----------------------|
| Pages/Articles | [20190820][]     | [Articles latest][]   |
 

[20190820]: https://dumps.wikimedia.org/simplewiki/20190820/simplewiki-20190820-pages-articles.xml.bz2
[20190824]: https://dumps.wikimedia.org/other/categoriesrdf/20190824/simplewiki-20190824-categories.ttl.gz

[Articles latest]: https://dumps.wikimedia.org/simplewiki/
[Categories latest]: https://dumps.wikimedia.org/other/categoriesrdf/latest


See also https://codito.in/simple-wikipedia-dataset

**License**
Same license as upstream wikipedia datasets.

> All text content is multi-licensed under the Creative Commons
> Attribution-ShareAlike 3.0 License (CC-BY-SA) and the GNU Free Documentation
> License (GFDL).

See https://en.wikipedia.org/wiki/Wikipedia:Database_download

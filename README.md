# Инвертированный индекс
Приложение на Python, которое предоставляет консольный интерфейс для:
- построения инвертированного индекса и эффективного сохранения его
на диске с помощью модуля struct;
- поиска по инвертированному индексу в кодировках utf-8 и cp1251.

Приложение (inverted_index.py) должно предоставлять следующий CLI:  
1. Построение инвертированного индекса на основе датасета (см. формат ниже) и его эффективное сжатие для сохранения на диск:
`$ python3 inverted_index.py build --dataset /path/to/dataset --output /path/to/inverted.index`
2. Реализация поиска со следующим консольным интерфейсом:  
`$ python3 inverted_index.py query --index /path/to/inverted.index --query-file-utf8 /path/to/quries.txt`  
`$ cat /path/to/quries.txt | python3 inverted_index.py query --index /path/to/inverted.index --query-file-utf8 -`  
`$ python3 inverted_index.py query --index /path/to/inverted.index --query-file-cp1251 /path/to/quries.txt`  
`$ python3 inverted_index.py query --index /path/to/inverted.index --query first query [--query the second query]`  

Входные данные:  
- файл доступен в режиме read-only в локальной директории проекта;  
- в каждой строке: `article_ID(int) <tab> article_name <spaces> article_content`.

Выходной формат “обстрела”:  
- по результатам “обстрела” stdout должен содержать только ответы на запросы;  
- запрос в файле: “long query”, состоит из двух слов “long” и “query”;  
- допустим в датасете только 3 документа 151, 13, 3998 содержат одновременно оба этих слова, тогда ваш ответ: “151,13,3998”. Порядок предоставленных документов в ответе не важен (может быть любым).

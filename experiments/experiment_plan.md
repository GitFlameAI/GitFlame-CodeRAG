# Retrieval Experiment Plan

## Что Сравниваем

| Experiment | Pipeline | Зачем сравниваем |
|---|---|---|
| `bm25_only` | BM25 | Lexical baseline. |
| `dense_only` | Dense | Semantic baseline. |
| `ast_only` | AST | Structural/symbol baseline. |
| `bm25_dense_rrf` | BM25 + Dense -> RRF | Проверяем пользу hybrid lexical + semantic retrieval. |
| `bm25_ast_rrf` | BM25 + AST -> RRF | Проверяем пользу AST поверх lexical retrieval. |
| `dense_ast_rrf` | Dense + AST -> RRF | Проверяем semantic + structural retrieval. |
| `full_rrf` | BM25 + Dense + AST -> RRF | Основной hybrid retrieval без reranker. |
| `full_rrf_reranker` | BM25 + Dense + AST -> RRF -> Reranker | Финальный полный pipeline. |

## Метрики

| Метрика | Зачем измеряем |
|---|---|
| `Recall@K` | Главная метрика: показывает, нашли ли нужные файлы/chunks в top-k. |
| `Precision@K` | Показывает, насколько top-k не засорен нерелевантными chunks. |
| `MAP@K` | Показывает качество всего ranked list и насколько relevant chunks стабильно находятся высоко в выдаче. Важно, чтобы модель получала точный контекст и меньше галлюцинировала. |
| `Latency per issue` | Показывает, пригоден ли pipeline практически по скорости. |

## K И Параметры

| Что тестируем | Значения-кандидаты | Зачем |
|---|---|---|
| `final_top_k` | `5`, `10`, возможно `15` | Понять, сколько evidence chunks реально нужно отдавать дальше в LLM. |
| `bm25_top_k` | `20`, `50`, `100` | Проверить, сколько lexical candidates нужно до fusion. |
| `dense_top_k` | `20`, `50`, `100` | Проверить, сколько semantic candidates нужно до fusion. |
| `ast_top_k` | `20`, `50`, `100` | Проверить, сколько structural candidates нужно до fusion. |
| `rrf_k` | `10`, `30`, `60` | Понять чувствительность fusion к верхним позициям. |
| `rrf_top_k` | `20`, `50`, `100` | Определить размер candidate pool после fusion. |
| `reranker_top_k` | `20`, `50` | Понять, сколько кандидатов стоит отдавать cross-encoder-у. |
| `embedding_model` | lightweight vs code-specific | Сравнить скорость/качество dense retrieval. |

## Статистические Тесты

| Тест | Для чего | Как проводим | Как интерпретируем |
|---|---|---|---|
| `Cluster bootstrap CI` | Главный способ оценить устойчивость улучшения. | Для каждого repo считаем delta метрики между двумя методами, затем bootstrap-им 15 repo с replacement 5000-10000 раз. | Если 95% CI для delta не пересекает 0, улучшение устойчивое. |
| `Paired permutation / sign-flip test` | Основной p-value для сравнения двух методов. | Для каждого repo считаем delta, случайно меняем знак delta много раз и смотрим, насколько часто получаем улучшение не хуже наблюдаемого. | `p < 0.05` значит различие статистически значимо. |
| `Wilcoxon signed-rank` | Дополнительный paired-тест. | Применяем к 15 repo-level delta по `Recall@K`, `Precision@K`, `MAP@K`. | Используем как supporting evidence, не как единственный вывод. |
| `McNemar test` | Дополнительный sanity-check для binary `Recall@K`. | Для каждого issue: `1` = метод нашел relevant в top-k, `0` = не нашел. Сравниваем пары успех/провал для двух методов. | Если `p < 0.05`, один метод значимо чаще превращает провал в успех. Учитываем осторожно, потому что issues внутри repo зависимы. |
| `Holm-Bonferroni correction` | Защита от случайных значимых результатов при множественных сравнениях. | Применяем к p-values по нескольким сравнениям. | После correction значимыми считаем только оставшиеся `p < 0.05`. |


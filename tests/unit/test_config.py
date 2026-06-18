from gitflame_coderag.config.loader import parse_ai_config


def test_parse_ai_config_maps_nested_sections() -> None:
    config = parse_ai_config(
        {
            "analysis": {"include": ["src/**"], "exclude": ["dist/**"]},
            "chunking": {"max_chunk_lines": 40, "overlap_lines": 5},
            "retrieval": {"top_k": 8},
        }
    )

    assert config.include == ["src/**"]
    assert config.exclude == ["dist/**"]
    assert config.chunking.max_chunk_lines == 40
    assert config.retrieval.top_k == 8


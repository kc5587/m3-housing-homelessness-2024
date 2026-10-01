import json

from m3_analysis.run import build_outputs, main


def test_offline_reproduction_outputs_are_explicit_and_complete(tmp_path) -> None:
    build_outputs(tmp_path)
    result = json.loads((tmp_path / "results.json").read_text())
    assert result["historical_team_submission"] is True
    assert result["current_policy_forecast"] is False
    assert len(result["fits"]) == 6
    assert {row["year"] for row in result["forecasts"]} == {2034, 2044, 2074}
    assert len(tuple(tmp_path.glob("*.png"))) == 6
    assert (tmp_path / "appendix_data.csv").is_file()
    assert "not a confidence interval" in result["limitations"][0]


def test_cli_uses_requested_output_path(tmp_path, capsys) -> None:
    main(["--output-dir", str(tmp_path)])
    assert (tmp_path / "results.json").is_file()
    assert str(tmp_path) in capsys.readouterr().out

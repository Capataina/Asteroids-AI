"""
SAC-specific diagnostics report section.

Adds learner stability, action health, replay quality, representation health,
and evaluation/generalization summaries for GNN-SAC runs.
"""

from typing import Dict, Any, List

from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def _has_sac_data(generations_data: List[Dict[str, Any]], config: Dict[str, Any]) -> bool:
    method = str(config.get("method", "")).lower()
    if "sac" in method:
        return True
    if not generations_data:
        return False
    return any(k.startswith("sac_") for k in generations_data[-1].keys())


def _bin_values(values: List[float], width: int) -> List[float]:
    if not values:
        return []
    width = max(1, min(width, len(values)))
    bins = []
    n = len(values)
    for i in range(width):
        start = int(i * n / width)
        end = int((i + 1) * n / width)
        chunk = values[start:end] or [values[start]]
        bins.append(sum(chunk) / len(chunk))
    return bins


def _sparkline(values: List[float], width: int) -> str:
    if not values:
        return "N/A"
    samples = _bin_values(values, width)
    if len(samples) < 2:
        return "." * len(samples)
    min_val = min(samples)
    max_val = max(samples)
    range_val = max_val - min_val
    if range_val == 0:
        return "." * len(samples)
    chars = " .:-=+*#%@"
    result = ""
    for v in samples:
        idx = int((v - min_val) / range_val * (len(chars) - 1))
        idx = max(0, min(len(chars) - 1, idx))
        result += chars[idx]
    return result


def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _phase_means(phases: List[Dict[str, Any]], key: str) -> List[float]:
    vals = []
    for phase in phases:
        series = [g.get(key, 0.0) for g in phase["data"]]
        vals.append(_mean(series))
    return vals


def _fmt(value: float, precision: int = 2) -> str:
    return f"{value:.{precision}f}"


def write_sac_diagnosis(f, generations_data: List[Dict[str, Any]], config: Dict[str, Any]) -> None:
    """Write the SAC diagnostics section."""
    if not _has_sac_data(generations_data, config):
        return

    f.write("## Graph Neural Network and Soft Actor-Critic Diagnosis\n\n")
    f.write("This section is generated only for GNN-SAC runs and summarizes learner health, replay quality,\n")
    f.write("representation stability, and evaluation behavior over time.\n\n")
    f.write("Note: SAC 'fitness' in the main report refers to training episode returns; evaluation is tracked separately.\n\n")

    if not generations_data:
        f.write("No SAC diagnostics available.\n\n")
        return

    latest = generations_data[-1]
    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)

    # --- Timebase & Evaluation ---
    f.write("### Run Timebase & Evaluation\n\n")
    f.write("| Metric | Latest | Notes |\n")
    f.write("|--------|--------|-------|\n")
    f.write(f"| Env Steps | {int(latest.get('sac_env_steps_total', 0)):,} | total environment steps |\n")
    f.write(f"| Updates | {int(latest.get('sac_updates_total', 0)):,} | total optimizer steps |\n")
    f.write(f"| Update/Data Ratio | {_fmt(latest.get('sac_update_to_data_ratio', 0.0), 3)} | updates per env step |\n")
    f.write(f"| Latest Eval Return | {_fmt(latest.get('sac_eval_return_mean', 0.0))} ± {_fmt(latest.get('sac_eval_return_std', 0.0))} | fixed seeds |\n")
    if "sac_eval_holdout_return_mean" in latest:
        f.write(
            f"| Holdout Eval Return | {_fmt(latest.get('sac_eval_holdout_return_mean', 0.0))} ± "
            f"{_fmt(latest.get('sac_eval_holdout_return_std', 0.0))} | held-out seeds |\n"
        )
    f.write(f"| Best Eval Return | {_fmt(latest.get('sac_eval_best_return', 0.0))} @ step {int(latest.get('sac_eval_best_step', 0)):,} | best so far |\n")
    f.write(f"| Eval Since Improve | {int(latest.get('sac_eval_since_improve', 0))} | eval cycles |\n")
    f.write("\n")

    if latest.get("sac_eval_returns"):
        f.write("Per-seed eval returns (latest):\n\n")
        f.write(f"`{latest.get('sac_eval_returns')}`\n\n")
    if latest.get("sac_eval_holdout_returns"):
        f.write("Per-seed holdout returns (latest):\n\n")
        f.write(f"`{latest.get('sac_eval_holdout_returns')}`\n\n")

    eval_series = [g.get("sac_eval_return_mean", 0.0) for g in generations_data if "sac_eval_return_mean" in g]
    if eval_series:
        f.write("```\n")
        f.write(f"Eval Return Trend  [{_sparkline(eval_series, 24)}]\n")
        f.write("```\n\n")

    holdout_series = [
        g.get("sac_eval_holdout_return_mean", 0.0)
        for g in generations_data
        if "sac_eval_holdout_return_mean" in g
    ]
    if holdout_series:
        f.write("```\n")
        f.write(f"Holdout Return Trend  [{_sparkline(holdout_series, 24)}]\n")
        f.write("```\n\n")

    # --- Learner Stability by Phase ---
    f.write("### Learner Stability by Phase\n\n")
    f.write("| Phase | Critic Loss | TD Abs p99 | Q Mean | Target Q Mean | Alpha | Critic Grad | Clip Rate |\n")
    f.write("|-------|-------------|------------|--------|----------------|-------|-------------|-----------|\n")
    for phase in phases:
        data = phase["data"]
        f.write(
            f"| {phase['label']} | "
            f"{_fmt(_mean([g.get('sac_critic_loss_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_td_abs_p99', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_q1_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_target_q_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_alpha_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_critic_grad_norm', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_critic_clip_rate', 0.0) for g in data]), 3)} |\n"
        )
    f.write("\n")

    # --- Action Health by Phase ---
    f.write("### Action Health by Phase\n\n")
    f.write("| Phase | Turn μ | Turn σ | Turn Sat | Thrust μ | Thrust σ | Thrust Sat | Shoot Rate | Shoot Sat |\n")
    f.write("|-------|--------|--------|----------|----------|----------|------------|-----------|-----------|\n")
    for phase in phases:
        data = phase["data"]
        f.write(
            f"| {phase['label']} | "
            f"{_fmt(_mean([g.get('sac_turn_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_turn_std', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_turn_saturation_rate', 0.0) for g in data]), 3)} | "
            f"{_fmt(_mean([g.get('sac_thrust_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_thrust_std', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_thrust_saturation_rate', 0.0) for g in data]), 3)} | "
            f"{_fmt(_mean([g.get('sac_shoot_rate', 0.0) for g in data]), 3)} | "
            f"{_fmt(_mean([g.get('sac_shoot_saturation_rate', 0.0) for g in data]), 3)} |\n"
        )
    f.write("\n")

    # --- Replay & Data Health ---
    f.write("### Replay & Data Health by Phase\n\n")
    f.write("| Phase | Replay Size | Ep Steps μ | Ep Steps p90 | Step Reward μ | Step Reward σ | Terminal μ | Terminal % |\n")
    f.write("|-------|-------------|------------|--------------|----------------|--------------|-------------|------------|\n")
    for phase in phases:
        data = phase["data"]
        f.write(
            f"| {phase['label']} | "
            f"{_fmt(_mean([g.get('sac_replay_size', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_episode_steps_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_episode_steps_p90', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_step_reward_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_step_reward_std', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_terminal_reward_mean', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_terminal_frac', 0.0) for g in data]), 3)} |\n"
        )
    f.write("\n")

    # --- Representation Health ---
    f.write("### Representation Health by Phase\n\n")
    f.write("| Phase | Embedding Norm | Dim Std | Cos Sim |\n")
    f.write("|-------|----------------|---------|---------|\n")
    for phase in phases:
        data = phase["data"]
        f.write(
            f"| {phase['label']} | "
            f"{_fmt(_mean([g.get('sac_embedding_norm', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_embedding_dim_std', 0.0) for g in data]))} | "
            f"{_fmt(_mean([g.get('sac_embedding_cos_sim', 0.0) for g in data]))} |\n"
        )
    f.write("\n")

    # --- Drift & Stability ---
    f.write("### Policy & Critic Drift (Latest)\n\n")
    f.write("| Metric | Value | Interpretation |\n")
    f.write("|--------|-------|----------------|\n")
    f.write(f"| Policy L1 Drift | {_fmt(latest.get('sac_policy_drift', 0.0))} | change on fixed probe set |\n")
    f.write(f"| Critic/Target Gap | {_fmt(latest.get('sac_critic_target_gap', 0.0))} | |Q - Q_target| on probe set |\n")
    f.write("\n")

    # --- Weight Distribution Snapshot ---
    f.write("### Weight Distribution Snapshot (Latest)\n\n")
    f.write("| Module | Mean | Std | Norm | Zero % |\n")
    f.write("|--------|------|-----|------|--------|\n")
    f.write(
        f"| GNN | {_fmt(latest.get('sac_gnn_weight_mean', 0.0), 4)} | "
        f"{_fmt(latest.get('sac_gnn_weight_std', 0.0), 4)} | "
        f"{_fmt(latest.get('sac_gnn_weight_norm', 0.0))} | "
        f"{_fmt(latest.get('sac_gnn_weight_zero_frac', 0.0) * 100, 2)}% |\n"
    )
    f.write(
        f"| Actor | {_fmt(latest.get('sac_actor_weight_mean', 0.0), 4)} | "
        f"{_fmt(latest.get('sac_actor_weight_std', 0.0), 4)} | "
        f"{_fmt(latest.get('sac_actor_weight_norm', 0.0))} | "
        f"{_fmt(latest.get('sac_actor_weight_zero_frac', 0.0) * 100, 2)}% |\n"
    )
    f.write(
        f"| Critic | {_fmt(latest.get('sac_critic_weight_mean', 0.0), 4)} | "
        f"{_fmt(latest.get('sac_critic_weight_std', 0.0), 4)} | "
        f"{_fmt(latest.get('sac_critic_weight_norm', 0.0))} | "
        f"{_fmt(latest.get('sac_critic_weight_zero_frac', 0.0) * 100, 2)}% |\n"
    )
    f.write("\n")

    # --- Takeaways & Warnings ---
    takeaways = [
        "Evaluation metrics are reported on fixed seeds and tracked separately from training returns.",
        "Critic stability is summarized via TD error tails and gradient/clip rates.",
        "Action saturation rates expose control collapse or oscillation.",
    ]
    write_takeaways(f, takeaways)

    warnings: List[str] = []
    if latest.get("sac_critic_clip_rate", 0.0) > 0.5:
        warnings.append("Critic gradients frequently exceed the clip threshold (high clip rate).")
    if latest.get("sac_embedding_cos_sim", 0.0) > 0.9:
        warnings.append("Embedding cosine similarity is very high (potential representation collapse).")
    if latest.get("sac_eval_since_improve", 0.0) >= 5:
        warnings.append("Evaluation has not improved for several eval cycles (possible stagnation).")
    write_warnings(f, warnings)

    write_glossary(
        f,
        glossary_entries([
            "sac_eval_return_mean",
            "sac_eval_return_std",
            "sac_eval_holdout_return_mean",
            "sac_eval_holdout_return_std",
            "sac_critic_loss_mean",
            "sac_td_abs_p99",
            "sac_alpha_mean",
            "sac_policy_entropy_mean",
            "sac_turn_saturation_rate",
            "sac_thrust_saturation_rate",
            "sac_shoot_saturation_rate",
            "sac_terminal_frac",
            "sac_embedding_cos_sim",
            "sac_policy_drift",
            "sac_critic_target_gap",
        ]),
        title="Glossary",
    )

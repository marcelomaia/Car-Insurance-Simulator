from domain.services.premium_calculation import (
    compute_applied_rate,
    compute_intrinsic_rate,
    compute_policy_limit_breakdown,
    compute_premium_breakdown,
)


def test_compute_applied_rate_adds_gis_variation():
    assert compute_applied_rate(0.01, 0.10) == 0.11


def test_compute_intrinsic_rate_matches_readme_decade_example():
    intrinsic = compute_intrinsic_rate(
        car_value=100_000.0,
        current_year=2026,
        rate_per_age_year=0.005,
        rate_per_value_chunk=0.005,
        value_chunk_size=10_000.0,
        vehicle_year=2016,
    )
    assert abs(intrinsic - 0.10) < 1e-9


def test_compute_intrinsic_rate_zero_age_when_vehicle_year_is_future():
    intrinsic = compute_intrinsic_rate(
        car_value=50_000.0,
        current_year=2020,
        rate_per_age_year=0.005,
        rate_per_value_chunk=0.005,
        value_chunk_size=10_000.0,
        vehicle_year=2030,
    )
    assert intrinsic == (50_000.0 / 10_000.0) * 0.005


def test_compute_policy_limit_breakdown_deductible_and_final():
    result = compute_policy_limit_breakdown(
        base_coverage_percentage=1.0,
        car_value=100_000.0,
        deductible_percentage=0.10,
    )
    assert result.base_policy_limit == 100_000.0
    assert result.deductible_value == 10_000.0
    assert result.policy_limit == 90_000.0


def test_compute_premium_breakdown_final_premium_formula():
    breakdown = compute_premium_breakdown(
        applied_rate=0.10,
        broker_fee=50.0,
        car_value=100_000.0,
        deductible_percentage=0.10,
    )
    assert breakdown.base_premium == 10_000.0
    assert breakdown.deductible_discount == 1_000.0
    assert breakdown.calculated_premium == 9_050.0

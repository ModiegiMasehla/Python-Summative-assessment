import pytest
from summative import *
import json
import copy


class TestSummative():

    ###################Question 1###################################
    @pytest.mark.parametrize("input_ids, expected_output", [
        (['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'],
         [['L1', 'L2', 'L3', 'L4', 'L5', 'L6'], ['L7']]),

        (['L1', 'L2', 'L3', 'L4', 'L5', 'L6'],
         [['L1', 'L2', 'L3', 'L4', 'L5', 'L6']]),

        (['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12'],
         [['L1', 'L2', 'L3', 'L4', 'L5', 'L6'], ['L7', 'L8', 'L9', 'L10', 'L11', 'L12']]),

        (['L1', 'L2', 'L3'], [['L1', 'L2', 'L3']]),

        (['L1'], [['L1']]),

        ([], []),

        (['1', '2', '3', '4', '5', '6', '7', '8'], [['1', '2', '3', '4', '5', '6'], ['7', '8']]),

        (['L10', 'L5', 'L3', 'L8', 'L1', 'L7', 'L2'],
         [['L10', 'L5', 'L3', 'L8', 'L1', 'L7'], ['L2']]),
    ])
    def test_batch_result_dispatcher_logic(self, input_ids, expected_output):
        assert batch_result_dispatcher(input_ids) == expected_output


    def test_batch_result_dispatcher_constraint_enforced(self):
        learner_ids = [f"L{i}" for i in range(1, 50)]
        result = batch_result_dispatcher(learner_ids)
        for batch in result:
            assert len(batch) <= 6, f"Batch exceeded limit: {batch}"


    def test_batch_result_dispatcher_no_data_loss(self):
        learner_ids = [f"L{i}" for i in range(1, 23)]
        result = batch_result_dispatcher(learner_ids)
        flattened = [item for batch in result for item in batch]
        assert flattened == learner_ids


    def test_batch_result_dispatcher_no_duplicates(self):
        learner_ids = [f"L{i}" for i in range(1, 18)]
        result = batch_result_dispatcher(learner_ids)
        flattened = [item for batch in result for item in batch]
        assert len(flattened) == len(set(flattened))


    def test_batch_result_dispatcher_order_preserved(self):
        learner_ids = [f"L{i}" for i in range(100, 115)]
        result = batch_result_dispatcher(learner_ids)
        flattened = [item for batch in result for item in batch]
        assert flattened == learner_ids


    def test_batch_result_dispatcher_returns_list_of_lists(self):
        result = batch_result_dispatcher(['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'])
        assert isinstance(result, list)
        for batch in result:
            assert isinstance(batch, list)


    def test_batch_result_dispatcher_tuple_input(self):
        result = batch_result_dispatcher(('L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'))
        assert result == [['L1', 'L2', 'L3', 'L4', 'L5', 'L6'], ['L7']]
        assert all(isinstance(batch, list) for batch in result)


    def test_batch_result_dispatcher_empty_returns_list(self):
        result = batch_result_dispatcher([])
        assert result == []
        assert isinstance(result, list)


    def test_batch_result_dispatcher_immutability(self):
        original = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        original_copy = original.copy()
        batch_result_dispatcher(original)
        assert original == original_copy, "Input list was mutated!"


    def test_batch_result_dispatcher_large_scale(self):
        large_input = [f"L{i}" for i in range(12000)]
        result = batch_result_dispatcher(large_input)

        assert len(result) == 2000
        assert all(len(batch) == 6 for batch in result)

        flattened = [item for batch in result for item in batch]
        assert flattened == large_input

    ###################Question 2###################################

    @pytest.mark.parametrize("days, expected", [
        ([], 0),
        (['R'], 0),
        (['D'], 1),
        (['R', 'R', 'R', 'R', 'R'], 0),
        (['D', 'D', 'D', 'D', 'D'], 5),

        (['D', 'D', 'D', 'R', 'R', 'R'], 3),

        (['R', 'R', 'R', 'D', 'D', 'D'], 3),

        (['R', 'D', 'D', 'D', 'D', 'R'], 4),

        (['D', 'D', 'R', 'D', 'D', 'D', 'R', 'D', 'D'], 3),
        (['D', 'R', 'D', 'D', 'R', 'D', 'D', 'D'], 3),
        (['R', 'D', 'D', 'D', 'D', 'D', 'D', 'R', 'D'], 6),

        (['D', 'R', 'D', 'R', 'D', 'R', 'D'], 1),
        (['R', 'D', 'R', 'D', 'R', 'D'], 1),

        (['D', 'D', 'R', 'D', 'D', 'R', 'D', 'D'], 2),

        (['R', 'D', 'R', 'D', 'D', 'R', 'D', 'D', 'D', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'D'], 3),
        (['D', 'D', 'R', 'R', 'D', 'D', 'D', 'D', 'R', 'D'], 4),
    ])
    def test_longest_dry_spell_logic(self, days, expected):
        assert longest_dry_spell(days) == expected


    @pytest.mark.parametrize("spell_length", [1, 2, 5, 10, 20, 50, 99, 100])
    def test_longest_dry_spell_exact_spell_surrounded_by_rain(self, spell_length):
        days = ['R', 'R'] + ['D'] * spell_length + ['R', 'R']
        assert longest_dry_spell(days) == spell_length

    @pytest.mark.parametrize("spell_length", [1, 3, 7, 13, 25, 50])
    def test_longest_dry_spell_two_spells_second_is_longer(self, spell_length):
        short_spell = ['D'] * (spell_length - 1) if spell_length > 1 else []
        long_spell = ['D'] * spell_length
        days = short_spell + ['R'] + long_spell
        assert longest_dry_spell(days) == spell_length

    @pytest.mark.parametrize("spell_length", [1, 3, 7, 13, 25, 50])
    def test_longest_dry_spell_two_spells_first_is_longer(self, spell_length):
        long_spell = ['D'] * spell_length
        short_spell = ['D'] * max(1, spell_length - 1)
        days = long_spell + ['R'] + short_spell
        assert longest_dry_spell(days) == spell_length

    @pytest.mark.parametrize("num_blocks, block_size", [
        (5, 3), (10, 4), (20, 2), (100, 1), (3, 10)
    ])
    def test_longest_dry_spell_repeating_blocks(self, num_blocks, block_size):
        days = (['D'] * block_size + ['R']) * num_blocks
        assert longest_dry_spell(days) == block_size

    def test_longest_dry_spell_large_scale_known_spell(self):
        filler = (['D', 'D', 'R']) * 100
        injected = ['D'] * 37
        days = filler + ['R'] + injected + ['R'] + filler
        assert longest_dry_spell(days) == 37

    def test_longest_dry_spell_large_all_dry(self):
        days = ['D'] * 10000
        assert longest_dry_spell(days) == 10000

    def test_longest_dry_spell_large_all_rain(self):
        days = ['R'] * 10000
        assert longest_dry_spell(days) == 0


    def test_longest_dry_spell_returns_int(self):
        assert isinstance(longest_dry_spell(['D', 'R', 'D']), int)

    def test_longest_dry_spell_returns_zero_not_none(self):
        result = longest_dry_spell([])
        assert result == 0
        assert isinstance(result, int)

    def test_longest_dry_spell_immutability(self):
        original = ['D', 'R', 'D', 'D', 'R']
        copy = original.copy()
        longest_dry_spell(original)
        assert original == copy, "Input list was mutated!"


    ###################Question 3###################################

    @pytest.mark.parametrize("prices, expected", [
        ([9, 6, 2, 9, 8, 4, 7, 8, 9], [2, 4]),

        ([5, 4, 3, 2, 1], []),
        ([1, 2, 3, 4, 5], []),

        ([6, 4, 2, 4, 6], [2]),

        ([10, 5, 10, 5, 10, 5, 10], [5, 5, 5]),
        ([2, 1, 2, 1, 2, 1, 2], [1, 1, 1]),

        ([5, 3, 1, 1, 3, 5], []),
        ([5, 1, 1, 5], []),

        ([1, 5, 10, 5, 1], []),

        ([6, 3, 5, 2, 4, 1, 7], [3, 2, 1]),

        ([8, 3, 8, 3, 8], [3, 3]),
        ([4, 6, 4, 6, 4, 6, 4], [4, 4]),

        ([9, 5, 8, 2, 7], [5, 2]),

        ([-1, -4, -2, -9, -5], [-4, -9]),

        ([3, -2, 1, -5, -3], [-2, -5]),
    ])
    def test_dip_finder_logic(self, prices, expected):
        assert dip_finder(prices) == expected


    @pytest.mark.parametrize("prices, reason", [
        ([], 'empty list'),
        ([5], 'single element — no neighbours'),
        ([10, 5], 'two elements — no middle element possible'),
        ([10, 5, 5], 'right plateau — not strictly lower than right neighbour'),
        ([5, 5, 10], 'left plateau — not strictly lower than left neighbour'),
        ([3, 3, 3], 'all equal'),
        ([5, 1, 1, 5], 'plateau in middle'),
    ])
    def test_dip_finder_returns_empty(self, prices, reason):
        result = dip_finder(prices)
        assert result == [], f"Expected [] for: {reason}"


    @pytest.mark.parametrize("dip_value, position", [
        (1, 1), (0, 2), (-5, 5), (10, 10), (50, 15)
    ])
    def test_dip_finder_single_injected_dip(self, dip_value, position):
        prices = list(range(dip_value + position, dip_value, -1))
        prices += [dip_value]
        prices += list(range(dip_value + 1, dip_value + position + 1))
        result = dip_finder(prices)
        assert result == [dip_value]

    @pytest.mark.parametrize("num_dips, high_value, low_value", [
        (3, 10, 1),
        (5, 50, 0),
        (10, 100, -5),
        (20, 999, 1),
    ])
    def test_dip_finder_known_number_of_dips(self, num_dips, high_value, low_value):
        prices = []
        for _ in range(num_dips):
            prices.extend([high_value, low_value])
        prices.append(high_value)

        result = dip_finder(prices)
        assert len(result) == num_dips
        assert all(p == low_value for p in result)

    @pytest.mark.parametrize("gap_size", [1, 2, 3, 5, 10])
    def test_dip_finder_dips_separated_by_gaps(self, gap_size):
        num_dips = 5
        high_val = 100
        low_val = 1
        prices = [high_val]
        for _ in range(num_dips):
            prices.append(low_val)
            prices.extend([high_val] * gap_size)

        result = dip_finder(prices)
        assert len(result) == num_dips
        assert all(p == low_val for p in result)

    def test_dip_finder_order_preserved(self):
        prices = [9, 1, 9, 3, 9, 2, 9, 4, 9]
        result = dip_finder(prices)
        assert result == [1, 3, 2, 4]

    def test_dip_finder_does_not_wrap_around(self):
        assert dip_finder([5, 9, 9, 9, 1]) == []
        assert dip_finder([1, 9, 9, 9, 5]) == []

    def test_dip_finder_large_scale_zigzag(self):
        prices = ([10, 1] * 500) + [10]
        result = dip_finder(prices)
        assert len(result) == 500
        assert all(p == 1 for p in result)

    def test_dip_finder_large_scale_no_dips(self):
        prices = list(range(10000))
        assert dip_finder(prices) == []


    def test_dip_finder_returns_list(self):
        assert isinstance(dip_finder([2, 1, 2]), list)

    def test_dip_finder_returns_list_on_empty(self):
        result = dip_finder([])
        assert result == []
        assert isinstance(result, list)

    def test_dip_finder_immutability(self):
        original = [95, 92, 94, 90, 93]
        copy = original.copy()
        dip_finder(original)
        assert original == copy, "Input list was mutated!"


    ################### Question 4 #########################
    @pytest.mark.parametrize("records, expected", [
        ([], {}),

        (
            [{"warning_id": "SAWS-001", "town": "Soweto", "municipality": "CoJ", "province": "Gauteng",
              "level": 2, "rainfall_mm": 12.5, "date": "2025-11-01", "start_time": "06:00",
              "end_time": "14:00", "status": "expired", "people_affected": 14200}],
            {"Level 2": 12.5}
        ),

        (
            [
                {"warning_id": "SAWS-001", "town": "Soweto", "municipality": "CoJ", "province": "Gauteng",
                 "level": 2, "rainfall_mm": 12.5, "date": "2025-11-01", "start_time": "06:00",
                 "end_time": "14:00", "status": "expired", "people_affected": 14200},
                {"warning_id": "SAWS-002", "town": "Sandton", "municipality": "CoJ", "province": "Gauteng",
                 "level": 2, "rainfall_mm": 7.5, "date": "2025-11-02", "start_time": "09:00",
                 "end_time": "15:00", "status": "expired", "people_affected": 8750},
            ],
            {"Level 2": 20.0}
        ),

        (
            [
                {"warning_id": "SAWS-001", "town": "Soweto", "municipality": "CoJ", "province": "Gauteng",
                 "level": 2, "rainfall_mm": 12.5, "date": "2025-11-01", "start_time": "06:00",
                 "end_time": "14:00", "status": "expired", "people_affected": 14200},
                {"warning_id": "SAWS-002", "town": "Sandton", "municipality": "CoJ", "province": "Gauteng",
                 "level": 4, "rainfall_mm": 85.0, "date": "2025-11-01", "start_time": "08:00",
                 "end_time": "16:00", "status": "expired", "people_affected": 8750},
            ],
            {"Level 2": 12.5, "Level 4": 85.0}
        ),

        (
            [
                {"warning_id": f"SAWS-00{i}", "town": f"Town {i}", "municipality": "CoJ", "province": "Gauteng",
                 "level": 1, "rainfall_mm": 4.0, "date": f"2025-11-0{i}", "start_time": "06:00",
                 "end_time": "10:00", "status": "expired", "people_affected": 5000}
                for i in range(1, 4)
            ],
            {"Level 1": 12.0}
        ),

        (
            [
                {"warning_id": "SAWS-001", "town": "Bellville", "municipality": "CoCT", "province": "Western Cape",
                 "level": 1, "rainfall_mm": 3.0, "date": "2025-11-01", "start_time": "09:00",
                 "end_time": "13:00", "status": "expired", "people_affected": 3200},
                {"warning_id": "SAWS-002", "town": "Khayelitsha", "municipality": "CoCT", "province": "Western Cape",
                 "level": 2, "rainfall_mm": 18.0, "date": "2025-11-01", "start_time": "10:00",
                 "end_time": "16:00", "status": "expired", "people_affected": 29500},
                {"warning_id": "SAWS-003", "town": "George", "municipality": "George", "province": "Western Cape",
                 "level": 3, "rainfall_mm": 40.0, "date": "2025-11-01", "start_time": "13:00",
                 "end_time": "20:00", "status": "expired", "people_affected": 21000},
            ],
            {"Level 1": 3.0, "Level 2": 18.0, "Level 3": 40.0}
        ),

        (
            [
                {"warning_id": "SAWS-001", "town": "Durban Central", "municipality": "eThekwini", "province": "KwaZulu-Natal",
                 "level": 4, "rainfall_mm": 95.0, "date": "2025-11-03", "start_time": "10:00",
                 "end_time": "18:00", "status": "expired", "people_affected": 33000},
                {"warning_id": "SAWS-002", "town": "Ladysmith", "municipality": "Alfred Duma", "province": "KwaZulu-Natal",
                 "level": 4, "rainfall_mm": 60.0, "date": "2025-11-03", "start_time": "13:00",
                 "end_time": "19:00", "status": "expired", "people_affected": 11200},
            ],
            {"Level 4": 155.0}
        ),

        (
            [
                {"warning_id": "SAWS-001", "town": "Soweto", "municipality": "CoJ", "province": "Gauteng",
                 "level": 2, "rainfall_mm": 1.1, "date": "2025-11-01", "start_time": "06:00",
                 "end_time": "10:00", "status": "expired", "people_affected": 5000},
                {"warning_id": "SAWS-002", "town": "Sandton", "municipality": "CoJ", "province": "Gauteng",
                 "level": 2, "rainfall_mm": 2.2, "date": "2025-11-02", "start_time": "08:00",
                 "end_time": "12:00", "status": "expired", "people_affected": 5000},
            ],
            {"Level 2": 3.3}
        ),
    ])
    def test_warning_summary_logic(self, records, expected):
        assert warning_summary(records) == expected



    def _make_record(self, i, level, rainfall_mm):
        """Helper to build a realistic full record."""
        return {
            "warning_id": f"SAWS-{i:05d}",
            "town": f"Town {i}",
            "municipality": "City of Johannesburg",
            "province": "Gauteng",
            "level": level,
            "rainfall_mm": rainfall_mm,
            "date": f"2025-11-{(i % 28) + 1:02d}",
            "start_time": "06:00",
            "end_time": "12:00",
            "status": "expired",
            "people_affected": 5000 + i
        }

    @pytest.mark.parametrize("level, num_records, mm_each", [
        (1,  5,  2.0),
        (2, 10,  1.5),
        (3,  3,  4.0),
        (4,  7,  0.5),
        (5, 20,  3.0),
    ])
    def test_warning_summary_single_level_computed_total(self, level, num_records, mm_each):
        records = [self._make_record(i, level, mm_each) for i in range(num_records)]
        expected_total = round(num_records * mm_each, 2)
        result = warning_summary(records)

        assert f"Level {level}" in result
        assert result[f"Level {level}"] == expected_total
        assert len(result) == 1


    @pytest.mark.parametrize("level_config", [
        {1: (5,  2.0), 2: (3,  1.5)},
        {2: (4,  3.0), 4: (6,  2.5), 5: (2,  5.0)},
        {1: (1,  1.0), 2: (2,  2.0), 3: (3,  3.0), 4: (4, 4.0)},
        {3: (10, 0.5), 5: (10, 0.5)},
        {1: (8,  1.25), 2: (5, 2.75), 3: (3, 0.5), 4: (7, 1.0), 5: (4, 3.5)},
    ])
    def test_warning_summary_multi_level_computed_totals(self, level_config):
        records = []
        idx = 0
        for level, (count, mm) in level_config.items():
            for _ in range(count):
                records.append(self._make_record(idx, level, mm))
                idx += 1

        result = warning_summary(records)

        assert len(result) == len(level_config)
        for level, (count, mm) in level_config.items():
            key = f"Level {level}"
            expected = round(count * mm, 2)
            assert key in result, f"{key} missing from result"
            assert result[key] == expected, f"{key}: expected {expected}, got {result[key]}"


    def test_warning_summary_no_phantom_levels(self):
        records = [
            self._make_record(0, 2, 2.0),
            self._make_record(1, 4, 3.0),
        ]
        result = warning_summary(records)
        assert set(result.keys()) == {"Level 2", "Level 4"}


    def test_warning_summary_zero_rainfall_still_listed(self):
        result = warning_summary([self._make_record(0, 1, 0.0)])
        assert result == {"Level 1": 0.0}


    def test_warning_summary_rounds_to_two_decimals(self):
        records = [self._make_record(i, 3, 0.1) for i in range(30)]
        result = warning_summary(records)
        assert result == {"Level 3": 3.0}


    def test_warning_summary_large_scale(self):
        levels = [1, 2, 3, 4]
        mm_each = 2.0
        records = [self._make_record(i, levels[i % 4], mm_each) for i in range(1000)]
        result = warning_summary(records)

        assert len(result) == 4
        for level in levels:
            expected = round(250 * mm_each, 2)
            assert result[f"Level {level}"] == expected


    def test_warning_summary_loaded_from_json(self):
        with open("weatherwarnings.json", "r") as f:
            records = json.load(f)

        result = warning_summary(records)

        expected = {}
        for record in records:
            key = f"Level {record['level']}"
            expected[key] = round(expected.get(key, 0) + record['rainfall_mm'], 2)

        assert isinstance(result, dict)
        assert all(k.startswith("Level ") for k in result.keys())
        assert result == expected



    def test_warning_summary_returns_dict(self):
        result = warning_summary([self._make_record(0, 2, 2.0)])
        assert isinstance(result, dict)

    def test_warning_summary_empty_returns_dict(self):
        result = warning_summary([])
        assert result == {}
        assert isinstance(result, dict)

    def test_warning_summary_values_are_numeric(self):
        result = warning_summary([self._make_record(0, 2, 2.0)])
        for val in result.values():
            assert isinstance(val, (int, float)), f"Expected numeric, got {type(val)}"

    def test_warning_summary_immutability(self):
        records = [
            self._make_record(0, 2, 2.5),
            self._make_record(1, 4, 4.0),
        ]
        original = copy.deepcopy(records)
        warning_summary(records)
        assert records == original, "Input was mutated!"


    ################### Question 5 #########################

    @pytest.mark.parametrize("size, expected", [
        (1, ["*"]),
        (2, [" *", "* *", " *"]),
        (3, ["  *", " * *", "*   *", " * *", "  *"]),
        (4, ["   *", "  * *", " *   *", "*     *", " *   *", "  * *", "   *"]),
        (5, ["    *", "   * *", "  *   *", " *     *", "*       *", " *     *", "  *   *", "   * *", "    *"]),
    ])
    def test_draw_diamond_logic(self, size, expected):
        assert draw_diamond(size) == expected


    @pytest.mark.parametrize("size", [1, 2, 3, 5, 8, 10, 15, 20, 50])
    def test_draw_diamond_returns_correct_number_of_rows(self, size):
        result = draw_diamond(size)
        assert len(result) == 2 * size - 1


    @pytest.mark.parametrize("size", [2, 3, 5, 8, 10, 15, 20])
    def test_draw_diamond_first_and_last_row_have_one_star(self, size):
        result = draw_diamond(size)
        assert result[0].strip() == "*"
        assert result[-1].strip() == "*"


    @pytest.mark.parametrize("size", [2, 3, 5, 8, 10, 15, 20])
    def test_draw_diamond_widest_row_is_in_the_middle(self, size):
        result = draw_diamond(size)
        expected_width = 2 * size - 1
        widest = result[size - 1]
        assert len(widest) == expected_width
        assert widest[0] == "*" and widest[-1] == "*"
        assert max(len(row) for row in result) == expected_width


    @pytest.mark.parametrize("size", [2, 3, 5, 8, 10, 15, 20])
    def test_draw_diamond_every_other_row_has_two_stars(self, size):
        result = draw_diamond(size)
        for i, row in enumerate(result[1:-1], start=2):
            star_count = row.count("*")
            assert star_count == 2, \
                f"Row {i} of size {size} should have 2 stars, got {star_count}: '{row}'"


    @pytest.mark.parametrize("size", [3, 5, 8, 10, 15, 20])
    def test_draw_diamond_top_half_inner_spaces(self, size):
        """Top half: the gap between the two stars on row i (0-based) must be 2*i - 1."""
        result = draw_diamond(size)
        for i in range(1, size):
            inner = result[i].strip()
            expected_inner = "*" + " " * (2 * i - 1) + "*"
            assert inner == expected_inner, \
                f"Row {i} size={size}: expected '{expected_inner}', got '{inner}'"


    @pytest.mark.parametrize("size", [2, 3, 5, 8, 10, 20])
    def test_draw_diamond_leading_spaces_decrease_then_increase(self, size):
        result = draw_diamond(size)
        leading = [len(row) - len(row.lstrip()) for row in result]
        assert leading[:size] == list(range(size - 1, -1, -1))
        assert leading[size - 1:] == list(range(0, size))


    @pytest.mark.parametrize("size", [1, 2, 3, 5, 8, 10, 20])
    def test_draw_diamond_is_vertically_symmetric(self, size):
        result = draw_diamond(size)
        assert result == result[::-1]


    @pytest.mark.parametrize("size", [3, 5, 8, 10, 20])
    def test_draw_diamond_peak_is_centred(self, size):
        """First row must have exactly size-1 leading spaces."""
        result = draw_diamond(size)
        expected_leading = size - 1
        actual_leading = len(result[0]) - len(result[0].lstrip())
        assert actual_leading == expected_leading, \
            f"size={size}: peak should have {expected_leading} leading spaces, got {actual_leading}"


    @pytest.mark.parametrize("size", [1, 2, 3, 5, 10])
    def test_draw_diamond_no_trailing_spaces(self, size):
        result = draw_diamond(size)
        for row in result:
            assert row == row.rstrip(), f"Row has trailing spaces: '{row}'"


    @pytest.mark.parametrize("size", [1, 2, 3, 5, 10])
    def test_draw_diamond_returns_list_of_strings(self, size):
        result = draw_diamond(size)
        assert isinstance(result, list)
        for row in result:
            assert isinstance(row, str), f"Each row must be a string, got {type(row)}"


    @pytest.mark.parametrize("size", [1, 2, 3, 5, 10])
    def test_draw_diamond_rows_contain_only_valid_chars(self, size):
        """Rows must only contain '*' and ' '."""
        result = draw_diamond(size)
        for row in result:
            for char in row:
                assert char in ("*", " "), f"Invalid character '{char}' in row: '{row}'"


    @pytest.mark.parametrize("size", [0, -1, -10])
    def test_draw_diamond_invalid_size(self, size):
        with pytest.raises(ValueError):
            draw_diamond(size)

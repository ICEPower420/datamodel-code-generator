from __future__ import annotations

from datamodel_code_generator.model.dataclass import DataClass, DataModelField
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.types import DataType, Types


def test_dataclass_without_frozen() -> None:
    """Test dataclass generation without frozen parameter."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        frozen=False,
    )

    rendered = dataclass.render()
    assert "@dataclass" in rendered
    assert "frozen=True" not in rendered
    assert "class TestModel:" in rendered


def test_dataclass_with_frozen() -> None:
    """Test dataclass generation with frozen=True."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        frozen=True,
    )

    rendered = dataclass.render()
    assert "@dataclass(frozen=True)" in rendered
    assert "class TestModel:" in rendered


def test_dataclass_with_keyword_only_and_frozen() -> None:
    """Test dataclass generation with both keyword_only and frozen parameters."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        keyword_only=True,
        frozen=True,
    )

    rendered = dataclass.render()
    assert "@dataclass" in rendered
    assert "kw_only=True" in rendered
    assert "frozen=True" in rendered
    assert "class TestModel:" in rendered


def test_dataclass_with_only_keyword_only() -> None:
    """Test dataclass generation with only keyword_only parameter."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        keyword_only=True,
        frozen=False,
    )

    rendered = dataclass.render()
    assert "@dataclass" in rendered
    assert "kw_only=True" in rendered
    assert "frozen=True" not in rendered
    assert "class TestModel:" in rendered


def test_dataclass_frozen_attribute() -> None:
    """Test that frozen attribute is properly stored."""
    reference = Reference(path="TestModel", name="TestModel")
    dataclass = DataClass(
        reference=reference,
        fields=[],
        frozen=True,
    )

    assert dataclass.frozen is True


def test_dataclass_frozen_false_attribute() -> None:
    """Test that frozen attribute defaults to False."""
    reference = Reference(path="TestModel", name="TestModel")

    dataclass = DataClass(
        reference=reference,
        fields=[],
    )

    assert dataclass.frozen is False


def test_dataclass_kw_only_true_only() -> None:
    """Test dataclass generation with kw_only=True only (comprehensive test)."""
    reference = Reference(path="TestModel", name="TestModel")
    field1 = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )
    field2 = DataModelField(
        name="field2",
        data_type=DataType(type=Types.integer),
        required=False,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field1, field2],
        keyword_only=True,
    )

    rendered = dataclass.render()
    # Should have @dataclass(kw_only=True) but not frozen=True
    assert "@dataclass(kw_only=True)" in rendered
    assert "frozen=True" not in rendered
    assert "class TestModel:" in rendered

    # Verify frozen attribute is False (default)
    assert dataclass.frozen is False
    assert dataclass.keyword_only is True


def test_dataclass_legacy_keyword_only() -> None:
    """Test that legacy 'frozen' argument is supported if dataclass_arguments is not set."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        keyword_only=True,
    )

    rendered = dataclass.render()
    assert "@dataclass(kw_only=True)" in rendered


def test_dataclass_legacy_frozen() -> None:
    """Test that legacy 'frozen' argument is supported if dataclass_arguments is not set."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        frozen=True,
    )

    rendered = dataclass.render()
    assert "@dataclass(frozen=True)" in rendered


def test_dataclass_with_custom_dataclass_arguments() -> None:
    """Test that custom dataclass_arguments are rendered correctly."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        dataclass_arguments={"slots": True, "repr": False, "order": True},
    )

    rendered = dataclass.render()
    assert "@dataclass(slots=True, order=True)" in rendered
    assert "repr=False" not in rendered


def test_dataclass_both_legacy_and_dataclass_arguments() -> None:
    """Test that dataclass_arguments take precedence over legacy flags."""
    reference = Reference(path="TestModel", name="TestModel")
    field = DataModelField(
        name="field1",
        data_type=DataType(type=Types.string),
        required=True,
    )

    dataclass = DataClass(
        reference=reference,
        fields=[field],
        frozen=True,  # legacy flag
        keyword_only=True,  # legacy flag
        dataclass_arguments={"frozen": False, "order": True},
    )

    rendered = dataclass.render()
    assert "@dataclass(order=True)" in rendered
    assert "@dataclass(frozen=False)" not in rendered
    assert "@dataclass(frozen=True)" not in rendered
    assert "@dataclass(kw_only=False)" not in rendered
    assert "@dataclass(kw_only=True)" not in rendered

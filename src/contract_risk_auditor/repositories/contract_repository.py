"""
Contract repository - data access for contracts table.
"""

from sqlalchemy.orm import Session

from contract_risk_auditor.domain.models.contract import Contract


class ContractRepository:
    """Data access for contracts."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_contract(self, filename: str, party_name: str) -> Contract:
        """Create a new contract entry."""
        contract = Contract(
            filename=filename,
            party_name=party_name,
        )
        self._session.add(contract)
        self._session.commit()
        self._session.refresh(contract)
        return contract

    def get_contract(self, contract_id: str) -> Contract | None:
        """Get a contract by ID."""
        return self._session.get(Contract, contract_id)

    def list_contracts(self, limit: int = 100) -> list[Contract]:
        """List all contracts."""
        return self._session.query(Contract).order_by(Contract.created_at.desc()).limit(limit).all()

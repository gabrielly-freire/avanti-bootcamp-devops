from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy import DateTime, Integer, String, Boolean, Date, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import db


class Medicine(db.Model):
    __tablename__ = "medicines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    fabricante: Mapped[str] = mapped_column(String(120), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    validade: Mapped[datetime] = mapped_column(Date, nullable=True)
    receita_obrigatoria: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    itens_venda: Mapped[List["SaleItem"]] = relationship("SaleItem", back_populates="medicamento")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nome": self.nome,
            "fabricante": self.fabricante,
            "preco": self.preco,
            "estoque": self.estoque,
            "validade": self.validade.isoformat() if self.validade else None,
            "receita_obrigatoria": self.receita_obrigatoria,
        }


class Sale(db.Model):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    itens: Mapped[List["SaleItem"]] = relationship("SaleItem", back_populates="venda", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "criado_em": self.criado_em.isoformat(),
            "total": self.total,
            "itens": [i.to_dict() for i in self.itens],
        }


class SaleItem(db.Model):
    __tablename__ = "sale_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venda_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), nullable=False)
    medicamento_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    venda: Mapped[Sale] = relationship("Sale", back_populates="itens")
    medicamento: Mapped[Medicine] = relationship("Medicine", back_populates="itens_venda")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "venda_id": self.venda_id,
            "medicamento_id": self.medicamento_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
        }


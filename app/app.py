from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List

from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import BadRequest, NotFound

from app.database import init_db, db
from app.models import Medicine, Sale, SaleItem


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharmacy.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app)
    register_routes(app)
    return app


def parse_date(value: Any) -> date | None:
    if value in (None, "", "null"):
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value).date()
    except Exception as e:
        raise BadRequest(f"Data inválida: {value}") from e


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/v1/health")
    def health():
        return jsonify({"ok": True})

    @app.get("/api/medicamentos")
    def list_medicines():
        itens = Medicine.query.order_by(Medicine.nome.asc()).all()
        return jsonify([m.to_dict() for m in itens])

    @app.post("/api/medicamentos")
    def create_medicine():
        data: Dict[str, Any] = request.get_json(force=True, silent=False) or {}
        required = ["nome", "fabricante", "preco", "estoque"]
        for k in required:
            if k not in data:
                raise BadRequest(f"Campo obrigatório ausente: {k}")
        m = Medicine(
            nome=str(data["nome"]).strip(),
            fabricante=str(data["fabricante"]).strip(),
            preco=float(data.get("preco", 0.0)),
            estoque=int(data.get("estoque", 0)),
            validade=parse_date(data.get("validade")),
            receita_obrigatoria=bool(data.get("receita_obrigatoria", False)),
        )
        if m.preco < 0 or m.estoque < 0:
            raise BadRequest("Preço e estoque devem ser não negativos")
        db.session.add(m)
        db.session.commit()
        return jsonify(m.to_dict()), 201

    @app.put("/api/medicamentos/<int:mid>")
    def update_medicine(mid: int):
        m = Medicine.query.get(mid)
        if not m:
            raise NotFound("Medicamento não encontrado")
        data: Dict[str, Any] = request.get_json(force=True, silent=False) or {}
        if "nome" in data:
            m.nome = str(data["nome"]).strip()
        if "fabricante" in data:
            m.fabricante = str(data["fabricante"]).strip()
        if "preco" in data:
            m.preco = float(data["preco"])
        if "estoque" in data:
            novo_estoque = int(data["estoque"])
            if novo_estoque < 0:
                raise BadRequest("Estoque não pode ser negativo")
            m.estoque = novo_estoque
        if "validade" in data:
            m.validade = parse_date(data["validade"])
        if "receita_obrigatoria" in data:
            m.receita_obrigatoria = bool(data["receita_obrigatoria"])
        if m.preco < 0:
            raise BadRequest("Preço não pode ser negativo")
        db.session.commit()
        return jsonify(m.to_dict())

    @app.delete("/api/medicamentos/<int:mid>")
    def delete_medicine(mid: int):
        m = Medicine.query.get(mid)
        if not m:
            raise NotFound("Medicamento não encontrado")
        if m.itens_venda:
            raise BadRequest("Não é possível excluir medicamento com vendas associadas")
        db.session.delete(m)
        db.session.commit()
        return jsonify({"ok": True})

    @app.post("/api/vendas")
    def create_sale():
        payload: Dict[str, Any] = request.get_json(force=True, silent=False) or {}
        itens: List[Dict[str, Any]] = payload.get("itens", [])
        if not itens:
            raise BadRequest("A venda precisa de pelo menos um item")

        medicamentos: Dict[int, Medicine] = {}
        total = 0.0
        venda = Sale(total=0.0)
        db.session.add(venda)

        for item in itens:
            mid = int(item.get("medicamento_id"))
            qtd = int(item.get("quantidade", 1))
            if qtd <= 0:
                raise BadRequest("Quantidade deve ser maior que zero")
            med = medicamentos.get(mid) or Medicine.query.get(mid)
            if not med:
                raise BadRequest(f"Medicamento {mid} não encontrado")
            if med.validade and med.validade < date.today():
                raise BadRequest(f"Medicamento {med.nome} está vencido")
            if med.estoque < qtd:
                raise BadRequest(f"Estoque insuficiente para {med.nome}")
            preco_unit = float(item.get("preco_unitario", med.preco))
            if preco_unit < 0:
                raise BadRequest("Preço unitário inválido")
            med.estoque -= qtd
            total_item = preco_unit * qtd
            total += total_item
            si = SaleItem(
                venda=venda, medicamento=med, quantidade=qtd, preco_unitario=preco_unit
            )
            db.session.add(si)
            medicamentos[mid] = med

        venda.total = round(total, 2)
        db.session.commit()
        return jsonify(venda.to_dict()), 201

    @app.get("/api/vendas")
    def list_sales():
        vendas = Sale.query.order_by(Sale.criado_em.desc()).limit(50).all()
        return jsonify([v.to_dict() for v in vendas])


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

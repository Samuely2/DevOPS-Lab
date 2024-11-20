// api/categorias.js
module.exports = (req, res) => {
    const categorias = [
      { id: '1', nome: 'Categoria 1', descricao: 'Descrição 1' },
      { id: '2', nome: 'Categoria 2', descricao: 'Descrição 2' }
    ];
    res.status(200).json(categorias);
  };
  
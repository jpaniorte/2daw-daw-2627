function saludo(r) {
    r.return(200, `Hola desde njs. Has pedido ${r.uri} con ${r.method}\n`);
}
export default { saludo };

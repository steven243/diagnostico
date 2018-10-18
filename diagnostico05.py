#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 13:01:16 2018

@author: juancastro
"""

from flask import Flask,jsonify,request
from random import choice
from pyknow import *

app = Flask(__name__)

"""
100 Diabetes
101 Orina constante
102 Sed Constante
103 Hambre Excesiva
"""

class Sintoma(Fact):
    pass

class Enfermedad(Fact):
    pass

class DiagnosticoEnfermedad(KnowledgeEngine):

    @Rule(AND(Sintoma(codigo=101),
              Sintoma(codigo=102),
              Sintoma(codigo=103)
    ))
    def regla1(self):
        self.declare(Enfermedad(codigo=100,nombre='Diabetes'))


    @Rule(AND(Sintoma(codigo=201),
              Sintoma(codigo=202),
              Sintoma(codigo=203)
    ))
    def regla2(self):
        self.declare(Enfermedad(codigo=200,nombre='Colesterol'))


    @Rule(AND(Sintoma(codigo=301),
              Sintoma(codigo=302),
              Sintoma(codigo=303)
    ))
    def regla3(self):
        self.declare(Enfermedad(codigo=300,nombre='Gastritis'))

@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    data_json = request.json
    sintomas = data_json['sintomas']

    watch('RULES', 'FACTS')
    engine = DiagnosticoEnfermedad()
    engine.reset()
    
    for code in sintomas:
        engine.declare(Sintoma(codigo=code))    
        
    engine.run()
    diagnostico = engine.facts   

    codigo = 0
    nombre = ""
    for d in diagnostico:
        if (type(diagnostico[d]) == Enfermedad):
            codigo = diagnostico[d]['codigo']
            nombre = diagnostico[d]['nombre']
            
    respuesta = {'codigo':codigo, 'nombre':nombre}
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run()





package edu.rosehulman.xuez;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.semgraph.SemanticGraphEdge;
import edu.stanford.nlp.trees.GrammaticalRelation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.Pair;


public class NLP {

    /**
     * @param args
     * @throws IOException 
     */
    public static void main(String[] args) throws IOException {
    	
    	
    	//file IO
    	String input_path = "";
    	File folder = new File(input_path);
    	String[] fileList = folder.list();
    	Arrays.sort(fileList);
    	for (int i = 0; i < fileList.length; i++){
    		System.out.println(fileList.length);
    		String fileName = fileList[i];
    		InputStream in = new FileInputStream(input_path + "/"+fileName);
    		BufferedReader buff = new BufferedReader(new InputStreamReader(in));
    		String line= buff.readLine();
    		StringBuilder sb = new StringBuilder();
    		
    		while(line != null){
    			sb.append(line).append("\n");
    			line = buff.readLine();
    		}
    		
    		String text = sb.toString();
    		System.out.println(text);
    		if(text.equals(" exit")) break;
    		naturalLanguageProcess(text);
    	}
    	
       



    }
    
    static public void naturalLanguageProcess(String text){
    	 Properties props = new Properties();
         props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");

  
         StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
         // read some text in the text variable
//         String text = " Pick up that block"; 

         // create an empty Annotation just with the given text
         Annotation document = new Annotation(text);
         
         // run all Annotators on this text
         pipeline.annotate(document);
         
         // these are all the sentences in this document
         // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
         List<CoreMap> sentences = document.get(SentencesAnnotation.class);
         
         for(CoreMap sentence: sentences) {
           // traversing the words in the current sentence
           // a CoreLabel is a CoreMap with additional token-specific methods
           for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
             // this is the text of the token
             String word = token.get(TextAnnotation.class);
             // this is the POS tag of the token
             String pos = token.get(PartOfSpeechAnnotation.class);
             // this is the NER label of the token
             String ne = token.get(NamedEntityTagAnnotation.class);
//             System.out.println("word " + word + " ,pos: " + pos + " ,ne: " + ne);
           }


//           // this is the Stanford dependency graph of the current sentence
           SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
           System.out.println();
           System.out.println(dependencies);

           // get root of parse graph
           IndexedWord root = dependencies.getFirstRoot();
           // type of root
           String type = root.tag();
           switch (type) {
 	          case "VB": processVerbPhrase(dependencies, root); break;
 	          case "NN": processNounPhrase(dependencies, root); break;
 	          case "DT": processDeterminer(dependencies, root); break;
 	          default: System.out.println("Cannot identify sentence structure.");
           }
           // next step, need to identify further components of sentence

           


         }
    }

    // Processes: {This, that} one?
    static public void processDeterminer(SemanticGraph dependencies, IndexedWord root){
        List<Pair<GrammaticalRelation,IndexedWord>> s = dependencies.childPairs(root);

        System.out.println("Identity of object: " + root.originalText().toLowerCase());
      }
    
    //Processes: {That, this, the} {block, sphere}
    static public void processNounPhrase(SemanticGraph dependencies, IndexedWord root){
      List<Pair<GrammaticalRelation,IndexedWord>> s = dependencies.childPairs(root);

      System.out.println("Identity of object: " + root.originalText().toLowerCase());
      System.out.println("Type of object: " + s.get(0).second.originalText().toLowerCase());
    }
    
    // Processes: {Pick up, put down} {that, this} {block, sphere}
    static public void processVerbPhrase(SemanticGraph dependencies, IndexedWord root){
        List<Pair<GrammaticalRelation,IndexedWord>> s = dependencies.childPairs(root);
        Pair<GrammaticalRelation,IndexedWord> prt = s.get(0);
        Pair<GrammaticalRelation,IndexedWord> dobj = s.get(1);
        
        List<Pair<GrammaticalRelation,IndexedWord>> newS = dependencies.childPairs(dobj.second);
        
        System.out.println("Action: " + root.originalText().toLowerCase() + prt.second.originalText().toLowerCase());
        System.out.println("Type of object: " + dobj.second.originalText().toLowerCase());
        System.out.println("Identity of object: " + newS.get(0).second.originalText().toLowerCase());
      }

}
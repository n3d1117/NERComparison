import Foundation
import NaturalLanguage

func namedEntities(in string: String) -> [String] {
	var entities: [String] = []
	let tagger = NLTagger(tagSchemes: [.nameType])
	tagger.string = string
	tagger.enumerateTags(in: string.startIndex..<string.endIndex, unit: .word, scheme: .nameType, options: [.joinNames]) { (tag, range) -> Bool in
		switch tag {
		case .personalName?, .placeName?, .organizationName?:
			entities.append(String(string[range]))
		default: break
		}
		return true
	}
	return entities
}

func json(_ array: [String]) -> String {
	guard let data = try? JSONSerialization.data(withJSONObject: array, options: []) else { return "" }
	return String(data: data, encoding: String.Encoding.utf8)!
}

let path = Bundle.main.path(forResource: "text", ofType: "txt")
let text = try String(contentsOfFile: path!, encoding: String.Encoding.utf8)
let entities = namedEntities(in: text)
print(json(entities))

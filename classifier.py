import json
from pathlib import Path


class ChromosomeClassifier:
    def __init__(self, dtw_engine):
        self.dtw = dtw_engine

    def classify(self, detections, class_names=None):
        """
        Classify chromosome detections into normal and ambiguous categories.
        """
        results = {
            'normal': [],
            'ambiguous': []
        }

        chromosome_names = {
            0: 'A1', 1: 'A2', 2: 'A3', 3: 'B4', 4: 'B5',
            5: 'C10', 6: 'C11', 7: 'C12', 8: 'C6', 9: 'C7',
            10: 'C8', 11: 'C9', 12: 'D13', 13: 'D14', 14: 'D15',
            15: 'E16', 16: 'E17', 17: 'E18', 18: 'F19', 19: 'F20',
            20: 'G21', 21: 'G22', 22: 'X', 23: 'Y'
        }

        x_count = len(detections.get(22, []))
        y_count = len(detections.get(23, []))

        for class_id in sorted(detections.keys()):
            count = len(detections[class_id])
            name = chromosome_names.get(class_id, f'Class_{class_id}')

            if class_id in [22, 23]:
                result = self._classify_sex_chromosome(class_id, count, name, x_count, y_count)
            else:
                result = self._classify_autosome(class_id, detections[class_id], count, name)

            if result['category'] == 'normal':
                results['normal'].append(result)
            else:
                results['ambiguous'].append(result)

        return results

    def _classify_autosome(self, class_id, chromosome_list, count, name):
        if count == 0:
            return {
                'category': 'ambiguous',
                'class_id': class_id,
                'name': name,
                'count': count,
                'reason': f'no chromosomes {name} detected',
                'description': f'numerical abnormality: no chromosomes {name} detected'
            }
        elif count == 1:
            return {
                'category': 'ambiguous',
                'class_id': class_id,
                'name': name,
                'count': count,
                'reason': f'only one chromosome {name} detected',
                'description': f'numerical abnormality: only one chromosome {name} detected'
            }
        elif count > 2:
            return {
                'category': 'ambiguous',
                'class_id': class_id,
                'name': name,
                'count': count,
                'reason': f'more than two chromosomes {name} detected',
                'description': f'numerical abnormality: more than two chromosomes {name} detected'
            }
        else:
            img1 = chromosome_list[0]['image']
            img2 = chromosome_list[1]['image']
            is_similar, similarity = self.dtw.is_similar(img1, img2)

            if is_similar:
                return {
                    'category': 'normal',
                    'class_id': class_id,
                    'name': name,
                    'count': count,
                    'dtw_similarity': round(similarity, 4)
                }
            else:
                return {
                    'category': 'ambiguous',
                    'class_id': class_id,
                    'name': name,
                    'count': count,
                    'dtw_similarity': round(similarity, 4),
                    'reason': 'chromosome pairs are not identical',
                    'description': f'structural abnormality: the chromosome {name} pairs are not identical'
                }

    def _classify_sex_chromosome(self, class_id, count, name, x_count, y_count):
        is_normal = (x_count == 1 and y_count == 1) or (x_count == 2 and y_count == 0)

        if is_normal:
            return {
                'category': 'normal',
                'class_id': class_id,
                'name': name,
                'count': count,
                'x_count': x_count,
                'y_count': y_count
            }
        else:
            return {
                'category': 'ambiguous',
                'class_id': class_id,
                'name': name,
                'count': count,
                'x_count': x_count,
                'y_count': y_count,
                'reason': 'numerical abnormality of sex chromosomes',
                'description': 'numerical abnormality of sex chromosomes'
            }

    def save_results(self, results, output_path):
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

    def print_summary(self, results):
        print("\n" + "=" * 50)
        print("CHROMOSOME CLASSIFICATION RESULTS")
        print("=" * 50)

        print(f"\nNormal: {len(results['normal'])} types")
        for item in results['normal']:
            print(f"  - {item['name']}: {item['count']} detected, DTW similarity: {item.get('dtw_similarity', 'N/A')}")

        print(f"\nAmbiguous: {len(results['ambiguous'])} types")
        for item in results['ambiguous']:
            print(f"  - {item['name']}: {item['description']}")

        print("\n" + "=" * 50)
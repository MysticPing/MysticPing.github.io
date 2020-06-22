require_relative "../../../backend/collector/importer"

describe Importer do
    describe "importer" do
        before (:all) do
            @im = Importer.new
            @apk_list = 
            [
                {
                    artikelid: 2,
                    namn: '4',
                    namn2: '5',
                    prisinklmoms: 6.00,
                    pant: 1.50,
                    volymiml: 700.0,
                    varugrupp: '8',
                    stil: '9',
                    alkoholhalt: 0.2,
                    sortiment: '10'
                }
            ]
            @expected_result = 
            [
                {
                    id: 2,
                    apk: 18.667, 
                    name: '4 5',
                    price: 7.5,
                    volume: 700.0,
                    style: '9',
                    type: '8',
                    abv: 0.2,
                    availability: '10'
                }
            ]
        end
        context "given array of hashes" do
            it "import and calculate data" do
                result = @im.import(@apk_list)
                expect(result).to eql(@expected_result)
            end
        end
    end
end
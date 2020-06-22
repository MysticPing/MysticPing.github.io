require_relative "../../../backend/collector/writer"

describe Importer do
    describe "importer" do
        before (:all) do
            @wr = Importer.new
            @data = 
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
        context "given data" do
            it "write to sql db" do
                result = @im.import(@apk_list)
                expect(result).to eql(@expected_result)
            end
        end
    end
end
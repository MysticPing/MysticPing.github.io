require_relative "../../backend/importer"

describe Importer do
    describe "importer" do
        before (:all) do
            @im = Importer.new
            @apk_list = 
            [
                {
                    artikelid: '2',
                    namn: '4',
                    namn2: '5',
                    prisinklmoms: '6.00',
                    pant: '1.50',
                    volymiml: '700',
                    varugrupp: '8',
                    stil: '9',
                    alkoholhalt: '20%',
                    sortiment: '10'
                },
                {
                    artikelid: '3',
                    namn: '4',
                    namn2: '5',
                    prisinklmoms: '12.00',
                    volymiml: '500',
                    varugrupp: '8',
                    stil: '9',
                    alkoholhalt: '40%',
                    sortiment: '10'
                },
            ]
            @expected_result = [[2, 18.667, '4 5', '7.5 kr', '700 ml', '8', '9', '20%', '10'],
                                [3, 16.667, '4 5', '12 kr', '500 ml', '8', '9', '40%', '10']]
            
            #insert.execute '2', '20', '4 5', '7 kr', '700 ml', '8', '9', '20%', '10'
            #insert.execute '3', '16.667', '4 5', '12 kr', '500 ml', '8', '9', '40%', '10'
        end
        context "given array of hashes" do
            it "create sql db" do
                test_db = @im.import(@apk_list, ":memory:")
                result = test_db.execute("select * from apk")
                expect(result).to eql(@expected_result)
            end
        end
    end
end